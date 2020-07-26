import json

"""
    This class will require the usage of classes from all models 
    Chances of a circular error occuring is high in this class
"""

class UserPermission:

    def __init__(self,user=None,isTeacher=False,
                 isAdmin=False,
                 isStaff=False,
                 createAssignment=False,
                 ):

        if user:
            self.grantPermission(user)


    @property
    def json(self):
        return self.__dict__



    @staticmethod
    def fromJsonString(data:str):
        return UserPermission(**json.loads(data))


    def __checkB2cUser(self,user):
        from home.models import OunceUser
        try:
            ounceuser=user.ounceUser
            self.has_b2c_permission=True
            if ounceuser.kyc_status == OunceUser.KYC_VERIFIED:
                self.verified_user_kyc=True
        except:
            return

    def __checkB2bUser(self,user):
        try:
            company=user.company
            self.has_b2b_permission=True
            if company.verificationstatus :
                self.verified_b2b=True
        except:
            return

    def __checkPractitioner(self,user):
        try:
            practitioner=user.professional
            self.has_connect_permission = True
            if practitioner.is_verified:
                self.verified_practitioner = True
        except:
            return


    def grantPermission(self,user):
        """
            --> check for practitioner access
            --> is verified patial user
        """

        self.__checkB2bUser(user)
        self.__checkB2cUser(user)
        self.__checkPractitioner(user)

    def __str__(self):
        return json.dumps(self.__dict__)



