from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Borrowers
from .serializers import BorrowerSerializer
from django.db.models import Sum
from tabulate import tabulate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

class BorrowerView(APIView):
    # API to add a new Borrower
    def post(self, request):
        brw = BorrowerSerializer(data=request.data)
        brw.is_valid(raise_exception=True)
        brw.save()
        return Response({
            "message":"Borrower Added Successfully!"
        })

    # API to view a list of ALL Borrowers
    def get(self,request):
        brw = Borrowers.objects.all()
        brwList = []
        for i in range(len(brw)):
            brwList.append(BorrowerSerializer(brw[i]).data)
        return Response(brwList)

class LoanView(APIView):
    # API that shows total money lended and amount recovered state by state.
    def get(self,request):
        brw = Borrowers.objects.values('state').annotate(amount_lended = Sum('loan_amt'), amount_recovered = Sum('amt_paid'))
        return Response(brw)

class StateLoansView(APIView):
    # this method is triggered to report via mail 10 AM evey day
    def send_mails_daily(self):
        brw = Borrowers.objects.values('state').annotate(amount_lended = Sum('loan_amt'), amount_recovered = Sum('amt_paid'))
        
        sender = 'your_email@gmail.com'
        password = 'your_password'
        server = 'smtp.gmail.com:587'
        receiver = 'your_email@gmail.com'

        text = """
        Hello, Sir.
        Statewise Loan Report:
        {table}
        Regards,
        {sender}"""

        html = """
        <html><body><p>Hello, Sir.</p>
        <p>Statewise Loan Report:</p>
        {table}
        <p>Regards,</p>
        <p>{sender}</p>
        </body></html>
        """

        data=[['Sr.No','State','Amount Lended','Amout Recovered']]

        for i in range(len(brw)):
            data.append([i+1,brw[i]['state'],brw[i]['amount_lended'],brw[i]['amount_recovered']])

        text = text.format(table=tabulate(data, headers="firstrow", tablefmt="grid"), sender=sender)
        html = html.format(table=tabulate(data, headers="firstrow", tablefmt="html"), sender=sender)

        message = MIMEMultipart(
            "alternative", None, [MIMEText(text), MIMEText(html,'html')])

        message['Subject'] = "Loan Report-Statwise "
        message['From'] = sender
        message['To'] = receiver
        server = smtplib.SMTP(server)
        server.ehlo()
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, message.as_string())
        server.quit()
        
        return None