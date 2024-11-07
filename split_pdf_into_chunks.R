# 载入必要的库
library(pdftools)

# 读取PDF文件的函数
split_pdf_into_chunks <- function(pdf_path, chunks) {
    # 获取原PDF的总页数
    total_pages <- pdf_length(pdf_path)
    
    # 计算每个分块的平均页数
    pages_per_chunk <- ceiling(total_pages / chunks)
    
    # 定义输出PDF的名称模式
    output_pattern <- gsub(".pdf", "", basename(pdf_path))
    
    # 开始拆分PDF
    for(i in seq_len(chunks)) {
        # 计算当前块的起始和结束页
        start_page <- (i - 1) * pages_per_chunk + 1
        end_page <- min(i * pages_per_chunk, total_pages)
        
        # 定义当前块的PDF文件名
        output_pdf_path <- sprintf("%s_chunk_%02d.pdf", output_pattern, i)
        
        # 如果起始页大于总页数，则不再继续
        if (start_page > total_pages) {
            break
        }
        
        # 使用pdf_subset来创建新的PDF
        pdf_subset(pdf_path, pages = start_page:end_page, output = output_pdf_path)
        
        # 打印状态消息
        cat(sprintf("Chunk %d: pages %d to %d written to %s\n", i, start_page, end_page, output_pdf_path))
    }
}

# 实际调用函数进行PDF的拆分
# PDF路径为"D:\\ContributeToOtherGuys\\outline-2023\\outline_fungi_2023.pdf"，我们想要将其拆分成4个部分
split_pdf_into_chunks('D:\\ContributeToOtherGuys\\outline-2023\\outline_fungi_2023.pdf', 4)
