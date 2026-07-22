from rest_framework.throttling import UserRateThrottle


class LoginRateThrottle(UserRateThrottle):
    scope = "login"


class RegisterRateThrottle(UserRateThrottle):
    scope = "register"


class ProductRateThrottle(UserRateThrottle):
    scope = "products"


class OrderRateThrottle(UserRateThrottle):
    scope = "orders"


class PaymentRateThrottle(UserRateThrottle):
    scope = "payments"
