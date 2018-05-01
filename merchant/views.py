import braintree
from braintree import Transaction
from braintree.environment import Environment

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ViewSet


class MerchantViewSet(ViewSet):

    BRAINTREE_MERCHANT_ID = 'sr38wtsmhkvqrnmc'
    BRAINTREE_PUBLIC_KEY = 'srzzpwcvynb3zjcr'
    BRAINTREE_PRIVATE_KEY = '96c30c931d91ca6eef6ff7509022ab41'

    def configure_braintree(self):
        sandbox = Environment(
            'sandbox',
            'api.sandbox.braintreegateway.com',
            '443',
            'https://auth.sandbox.venmo.com',
            True,
            Environment.braintree_root() + '/ssl/api_braintreegateway_com.ca.crt'
        )

        braintree.Configuration.configure(
            environment=sandbox,
            merchant_id=self.BRAINTREE_MERCHANT_ID,
            public_key=self.BRAINTREE_PUBLIC_KEY,
            private_key=self.BRAINTREE_PRIVATE_KEY
        )

    @action(detail=False, methods=['GET', 'POST'])
    def get_braintree_client_token(self, request):
        self.configure_braintree()

        if request.method == 'GET':
            braintree_client_token = braintree.ClientToken.generate()
            response = {'braintreeClientToken': braintree_client_token, 'status': HTTP_200_OK}
            return Response(response, status=response['status'])

        else:
            body = request.data
            return Response(body, status=HTTP_200_OK)

    @action(detail=False, methods=['POST'])
    def payment(self, request):
        self.configure_braintree()

        body = request.data
        payment_method_nonce = body.get('payment_method_nonce')
        amount = body.get('amount')

        result = Transaction.sale({
            'amount': amount,
            'payment_method_nonce': payment_method_nonce,
            'options': {
                'submit_for_settlement': True
            }
        })

        if result.is_success:
            response = {'braintreeTransactionID': result.transaction.id, 'status': HTTP_200_OK}
            return Response(response, status=response['status'])
        else:
            response = {'message': result.message, 'reason': result.errors.deep_errors, 'status': HTTP_400_BAD_REQUEST}
            return Response(response, status=response['status'])
