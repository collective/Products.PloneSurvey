# HTML2PDF - converts HTML to PDF
# needs xhtml2pdf on the path ( http://www.xhtml2pdf.com/ )

import AccessControl, cgi, os

def html2pdf(self, html="<html></html>"):
    """ html2pdf converts a HTML-Page to a PDF-Document """

    securityContext=AccessControl.getSecurityManager()
#    if securityContext.checkPermission('View', self):
    if 1:
        (stin,stout) = os.popen2('xhtml2pdf - -')
	stin.write(html.encode("utf-8"))
        stin.close()
        pdf = stout.read()
        stout.close()

        self.REQUEST.RESPONSE.setHeader('Content-type','application/pdf')
        self.REQUEST.RESPONSE.setHeader('Content-disposition','inline; filename="%s.pdf"' % (self.getId()))

        return pdf

    else:
        raise AccessControl.Unauthorized

