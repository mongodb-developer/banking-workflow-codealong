from django import forms
from .models import BankingDocument


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model = BankingDocument
        fields = ['title', 'content', 'document_type', 'customer_name', 'customer_id', 'status']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 8, 'placeholder': 'Paste or type the full document content here...'}),
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Loan Application – John Smith'}),
            'customer_name': forms.TextInput(attrs={'placeholder': 'e.g. John Smith'}),
            'customer_id': forms.TextInput(attrs={'placeholder': 'e.g. CUST-001'}),
        }


class SearchForm(forms.Form):
    query = forms.CharField(
        max_length=500,
        label='Search Query',
        widget=forms.TextInput(attrs={'placeholder': 'e.g. mortgage loan requirements for first-time buyers'}),
    )
    document_type = forms.ChoiceField(
        choices=[('', 'All Types')] + BankingDocument.DOCUMENT_TYPES,
        required=False,
        label='Filter by Type',
    )
    limit = forms.IntegerField(
        min_value=1,
        max_value=20,
        initial=5,
        required=False,
        label='Results',
    )


class RAGQueryForm(forms.Form):
    question = forms.CharField(
        max_length=1000,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'placeholder': 'e.g. What are the outstanding compliance issues for customer CUST-007?',
        }),
        label='Your Question',
    )
    document_type = forms.ChoiceField(
        choices=[('', 'All Types')] + BankingDocument.DOCUMENT_TYPES,
        required=False,
        label='Limit to Document Type',
    )
