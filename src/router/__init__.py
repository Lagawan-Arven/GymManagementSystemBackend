from src.router.system_router import router as SystemRouter
from src.router.auth_router import router as AuthRouter
from src.router.admin_router import router as AdminRouter
from src.router.member_router import router as MemberRouter
from src.router.session_router import router as SessionRouter
from src.router.payment_router import router as PaymentRouter
from src.router.logs_router import router as LogsRouter

__all__ = [SystemRouter,AuthRouter,AdminRouter,MemberRouter,SessionRouter,PaymentRouter,LogsRouter]
