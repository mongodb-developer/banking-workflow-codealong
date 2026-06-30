from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import BankingDocument, WorkflowTask
from .forms import DocumentUploadForm, SearchForm, RAGQueryForm
from .services.embedding_service import generate_embedding
from .services.vector_search_service import semantic_search
from .services.rag_service import answer_query


# Lists all documents with optional type/status filtering.
def document_list(request):
    documents = BankingDocument.objects.all()
    doc_type = request.GET.get('type')
    status = request.GET.get('status')

    if doc_type:
        documents = documents.filter(document_type=doc_type)
    if status:
        documents = documents.filter(status=status)

    context = {
        'documents': documents,
        'document_types': BankingDocument.DOCUMENT_TYPES,
        'status_choices': BankingDocument.STATUS_CHOICES,
        'current_type': doc_type,
        'current_status': status,
    }
    return render(request, 'banking/document_list.html', context)



# Handles document upload, embedding generation, and workflow task creation.
def document_upload(request):
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST)
        if form.is_valid():
            document = form.save(commit=False)
            # TODO: Generate embedding for the document
            # Combine title + content, call generate_embedding(), store in document.embedding
            # Use try/except so the document still saves if embedding fails
            document.save()
            _create_workflow_tasks(document)
            messages.success(request, f'Document "{document.title}" uploaded successfully.')
            return redirect('banking:document_list')
    else:
        form = DocumentUploadForm()
    return render(request, 'banking/document_upload.html', {'form': form})


def document_detail(request, pk):
    document = get_object_or_404(BankingDocument, pk=pk)
    tasks = document.tasks.all()
    return render(request, 'banking/document_detail.html', {
        'document': document,
        'tasks': tasks,
    })



# Semantic search using Voyage AI embeddings + MongoDB Atlas Vector Search.
def semantic_search_view(request):
    results = []
    form = SearchForm()

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            doc_type = form.cleaned_data.get('document_type') or None
            limit = form.cleaned_data.get('limit') or 5
            # TODO: Generate embedding for the query, then call semantic_search()
            # Store results in the 'results' variable
            # Wrap in try/except and show error message on failure

    return render(request, 'banking/search.html', {'form': form, 'results': results})



# RAG: retrieves relevant documents and builds context for the user's question.
def rag_query_view(request):
    answer = None
    sources = []
    form = RAGQueryForm()

    if request.method == 'POST':
        form = RAGQueryForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            doc_type = form.cleaned_data.get('document_type') or None
            # TODO: Call answer_query() with question and doc_type
            # Extract 'answer' and 'sources' from the result
            # Wrap in try/except and show error message on failure

    return render(request, 'banking/rag_query.html', {
        'form': form,
        'answer': answer,
        'sources': sources,
    })


def workflow_tasks(request):
    tasks = WorkflowTask.objects.filter(is_completed=False)
    return render(request, 'banking/workflow_tasks.html', {'tasks': tasks})


def complete_task(request, pk):
    task = get_object_or_404(WorkflowTask, pk=pk)
    task.is_completed = True
    task.completed_at = timezone.now()
    task.save()
    messages.success(request, f'Task "{task.get_task_type_display()}" marked as completed.')
    return redirect('banking:workflow_tasks')



# Maps document types to workflow tasks and creates them automatically.
def _create_workflow_tasks(document):
    task_map = {
        'loan_application': [
            ('document_review', 'Review loan application documents for completeness'),
            ('risk_assessment', 'Conduct risk assessment for loan applicant'),
            ('approval_request', 'Submit for final approval'),
        ],
        'kyc': [
            ('document_review', 'Verify identity documents'),
            ('compliance_check', 'Run compliance and AML checks'),
        ],
        'compliance': [
            ('compliance_check', 'Review compliance report and flag issues'),
        ],
        'account_statement': [
            ('document_review', 'Review account statement for anomalies'),
        ],
        'risk_assessment': [
            ('risk_assessment', 'Validate risk assessment methodology'),
            ('approval_request', 'Route to risk committee for approval'),
        ],
    }
    for task_type, description in task_map.get(document.document_type, []):
        WorkflowTask.objects.create(
            document=document,
            task_type=task_type,
            description=description,
        )
