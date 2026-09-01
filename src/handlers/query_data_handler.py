from handlers.command_handler import CommandHandler
from handlers.query_handler import QueryHandler
from models.request.get_files_list_request import GetFilesListRequest
from models.response.get_files_list_response import GetFilesResponse, GetFilesListResponse
from models.response.get_images_response import GetImageResponse, GetImagesListResponse, GetImagePageResponse

class QueryDataHandler:
    def __init__(self):
        self._qh = QueryHandler()
        self._ch = CommandHandler()

    async def get_files_list(self, filters: GetFilesListRequest):
        file_list = []
        start_date = filters.start_date
        end_date = filters.end_date
        files_list = self._qh.get_files_list(start_date, end_date)
        for file in files_list:
            data = GetFilesResponse(**file)
            file_list.append(data)
        response = GetFilesListResponse(files_list=file_list)
        return response

    async def get_images_from_file(self, file_uuid: str):
        data = []
        images = self._qh.get_images_by_uuid_file(file_uuid)
        for image in images:
            data.append(GetImageResponse(**image))
        response = GetImagesListResponse(files_list=data)
        return response

    async def get_image_page(self, file_uuid: str, page: int):
        total = self._qh.count_pages_by_file_uuid(file_uuid)
        image = self._qh.get_image_by_uuid_and_page(file_uuid, page)
        page_data = GetImageResponse(**image) if image else None
        return GetImagePageResponse(total_pages=total, page=page_data)