# from app.celery.celery_app import celery_app
# from app.celery.helpers import async_to_sync
# from app.utils.building_cache import get_building_cache, init_cache
# from app.utils.logger import log


# @celery_app.task
# @async_to_sync
# async def update_building_cache():
#     try:
#         log.info("babka bas")
#         await init_cache()

#     except Exception as er:
#         log.error(f"Some error: {er}")
#         return None
    
# @celery_app.task
# @async_to_sync
# async def get_b_cache():
#     try:
#         get_building_cache()
#         log.info(f"Some ")

#     except Exception as er:
#         log.error(f"Some error: {er}")
#         return None

