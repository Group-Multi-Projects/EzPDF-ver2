from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiExample, OpenApiParameter
from .serializers import FileSerializer, UploadFileSerializer

def upload_file_schema():
    return extend_schema(
        summary="Tải lên file và xử lý chuyển đổi",
        description="""
        API này cho phép tải file lên hệ thống và thực hiện các thao tác chuyển đổi dựa trên `request_type`:

        - `editfile`: Chuyển đổi PDF sang HTML và trích xuất nội dung
        - `pdf2word`: Chuyển đổi PDF sang Word
        - `pdf2html`: Chuyển đổi PDF sang HTML
        - `html2pdf`: Chuyển đổi HTML sang PDF

        **Lưu ý**: API này yêu cầu người dùng đăng nhập để liên kết file với tài khoản. Nếu không có tài khoản, hệ thống sẽ sử dụng `client` làm ID mặc định.
        """,
        parameters=[
            OpenApiParameter(
                name="file",
                description="Tệp tin cần tải lên (PDF, HTML, DOCX)",
                required=True,
                type={"type": "string", "format": "binary"}
            ),
            OpenApiParameter(
                name="request_type",
                description="Loại chuyển đổi mong muốn",
                required=True,
                type=str,
                enum=["editfile", "pdf2word", "pdf2html", "html2pdf"]
            )
        ],
        request=UploadFileSerializer,
        examples=[
            OpenApiExample(
                name="Chuyển đổi PDF sang Word",
                summary="Upload một file PDF và chuyển đổi sang Word",
                description="Ví dụ về việc tải lên một file PDF và chuyển đổi nó sang Word.",
                value={
                    "file": "/media/files/example.pdf",
                    "request_type": "pdf2word"
                },
                response_only=False
            ),
            OpenApiExample(
                name="Chuyển đổi HTML sang PDF",
                summary="Upload một file HTML và chuyển đổi sang PDF",
                description="Ví dụ về việc tải lên một file HTML và chuyển đổi nó sang PDF.",
                value={
                    "file": "/media/files/example.html",
                    "request_type": "html2pdf"
                },
                response_only=False
            )
        ],
        responses={
            201: {
                "description": "File đã được xử lý thành công",
                "content": {
                    "application/json": {
                        "example": {
                            "file": "/media/files/example.pdf",
                            "request_type": "pdf2word",
                            "output_file_url": "/media/files/converted_files/output-client-20240208123045.docx"
                        }
                    }
                }
            },
            400: {
                "description": "Yêu cầu không hợp lệ",
                "content": {
                    "application/json": {
                        "example": {
                            "error": "File không hợp lệ"
                        }
                    }
                }
            }
        }
    )
def file_schema():
    return extend_schema_view(
    list=extend_schema(
        summary="Danh sách tất cả các file",
        description="Trả về danh sách tất cả các file có trong hệ thống.",
    ),
    retrieve=extend_schema(
        summary="Lấy thông tin chi tiết một file",
        description="Lấy thông tin chi tiết của file dựa trên ID.",
    ),
    create=extend_schema(
        summary="Tải lên file mới",
        description="Cho phép người dùng tải file lên hệ thống.",
    ),
    update=extend_schema(
        summary="Cập nhật file",
        description="Cập nhật thông tin của một file cụ thể.",
    ),
    partial_update=extend_schema(
        summary="Cập nhật một phần file",
        description="Cập nhật một số trường của file mà không cần gửi toàn bộ dữ liệu.",
    ),
    destroy=extend_schema(
        summary="Xóa file",
        description="Xóa một file khỏi hệ thống.",
    ),
    files=extend_schema(
        summary="Lấy danh sách file chưa bị xóa",
        description="Trả về danh sách file chưa bị đưa vào thùng rác.",
    ),
    trashs=extend_schema(
        summary="Lấy danh sách file trong thùng rác",
        description="Trả về danh sách các file đã bị đưa vào thùng rác.",
    ),
    add_to_trash=extend_schema(
        summary="Di chuyển file vào thùng rác",
        description="Đánh dấu một file là đã bị xóa bằng cách đặt trường `trash` thành `True`.",
        request=None,
        responses={200: FileSerializer, 400: {"error": "File đã ở trong thùng rác"}, 404: {"error": "Không tìm thấy file"}},
    ),
)