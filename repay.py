from paynow import Paynow
import time

class Repay:
    def back(amount, phone):
        try:
            paynow = Paynow(
                "11336",
                "1f4b3900-70ee-4e4c-9df9-4a44490833b6",
                '127.0.0.1:5000/wasms',
                '127.0.0.1:5000/wasms'
            )

            payment = paynow.create_payment('Africa Century', 'faraimunashe.m11@gmail.com')

            payment.add('Loan settlement', amount)

            response = paynow.send_mobile(payment, phone, 'ecocash')

            timeout = 9
            count = 0

            if(response.success):

                while (True):
                    time.sleep(2)
                    pollUrl = response.poll_url
                    status = paynow.check_transaction_status(pollUrl)

                    if(status.paid):
                        return status.status
                    
                    count = count + 1
                    if (count > timeout):
                        return 'error'
        except:
            return 'error'


