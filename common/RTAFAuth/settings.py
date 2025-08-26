
AIRFORCE_AUTHENTICATION = {
    "url" : {        
        "AD" : "https://otp.rtaf.mi.th/api/v2/mfa/login",
        "HRIS" : "http://10.229.22.2:8080/api/RTAFHousePerson",
        "super_app":"https://app-native-services.rtaf.mi.th/gateway/Gr3VSUFxJDIIcTV4fFwww-api/salt-authorization?nouns=decrypt",        
    },
    "super_app_token":"2jREGkgg3vIQPxKmE1CpinmztnWWHRix1C4DqXLLoy6uFisfwPxwNMS9w1f5Exc28Lv6OxNWimrsHPQoQwdJhowZZ75tdJiI3272MaKDVPQxmfksFVYC5aljBYQ7yu81idXM4jsO2YaeFNLhdznU752A5GFYNJs8edhJu8dnNYPLnO83xLzopHyanVWluqSSzUUNGAZhWTgPMKlk7ZLkbFeOyYcgTCCpzoTfQ3xmEeOqXePClAAWHcRHt9qrLizk1fGeSpHHCNbPr4FdfUIuwZMbOVMNbB6Vdv4aKqnvPDa7",
    "allow_mode" : ["AD-Login", "RTAF-OTP-Login","SWC-AUTH-Login"], #  "RTAF-OTP-Login","SWC-AUTH-Login"
    "bypass_user" : [], #"pongthep",],
    "reload_AD_data_on_login" : True,
    "default" : {
        "is_active" : True,
        "groups" : [] #"UnitAdmin", "UnitStaff"
    },
    "update_user_function_AD" : "common.RTAFAuth.services.update_user_function_AD",
    "update_user_function_HRIS" : "common.RTAFAuth.services.update_user_function_HRIS",
}