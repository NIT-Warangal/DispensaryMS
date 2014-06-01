from xhtml2pdf import pisa             # import python module
from StringIO import StringIO
# Define your data
sourceHtml = ""
outputFilename = "test.pdf"

def create_pdf(pdf_data):
    pdf = StringIO()
    pisa.CreatePDF(StringIO(pdf_data.encode('utf-8')), pdf)
    return pdf
# Utility function
def convertHtmlToPdf(sourceHtml, outputFilename="test.pdf"):
    # open output file for writing (truncated binary)
    resultFile = open(outputFilename, "w+b")

    # convert HTML to PDF
    pisaStatus = pisa.CreatePDF(
            StringIO(sourceHtml.encode('utf-8')),                # the HTML to convert
            dest=resultFile)           # file handle to recieve result

    # close output file
    resultFile.close()                 # close output file

    # return True on success and False on errors
    return pisaStatus.err

# Main program
if __name__=="__main__":
    pisa.showLogging()
    convertHtmlToPdf(sourceHtml, outputFilename)
