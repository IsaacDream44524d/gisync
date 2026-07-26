from itsdangerous import URLSafeTimedSerializer as Serializer, SignatureExpired, BadSignature

class SecurityTokenMAnager:
    def __init__(self, secretKey):
        self.secretKey = secretKey
        self.reset_salt = 'reset_email'
        self.invite_salt = 'invite_email'

    def _getSerializer(self) -> Serializer:
        return Serializer(self.secretKey)

    def generateResetToken(self, userId):
        #create serializer using app secret key
        serializer = self._getSerializer()

        #turn data into secure token
        token = serializer.dumps({'userId': userId}, salt=self.reset_salt)
        return token
    
    def generateInviteToken(self, inviteId: int) -> str:
        #create serializer using app secret key
        serializer = self._getSerializer()

        #turn data into secure token
        token = serializer.dumps({'inviteId': inviteId}, salt=self.invite_salt)
        return token
    
    def verifyInviteToken(self, token: str, MAX_AGE: int = 604800):
        serializer = self._getSerializer()
        try:
            # invite is valid for a week = 7 days
            payload = serializer.loads(token, max_age=MAX_AGE, salt=self.invite_salt)
            return payload['inviteId']

        except (SignatureExpired, BadSignature):
            # display error or something
            return None

    def verifyResetToken(self, token: str, MAX_AGE: int = 1800) -> str:
        # deserialize/load data
        serializer = self._getSerializer()
        # token will expire after 30 minutes
        try:
            payload = serializer.loads(token, max_age=MAX_AGE, salt=self.reset_salt)
            return payload['userId']

        # put an error message here
        except (SignatureExpired, BadSignature):
            return None
        
