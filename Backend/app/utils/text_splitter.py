from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_into_chunks(text: str, 
                      chunk_size: int = 500, 
                      chunk_overlap: int = 50) -> list[str]:
    """
    Splits a long text into chunks of roughly chunk_size tokens (characters),
    with a bit of overlap so you don’t cut sentences in half.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)


