FROM ubuntu:24.04

RUN apt update
RUN apt -y install -f python3-pip wget

# Grab a version of wkhtmltox that can build
# the table of contents correctly
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-2/wkhtmltox_0.12.6.1-2.jammy_amd64.deb

RUN dpkg --force-all -i wkhtmltox_0.12.6.1-2.jammy_amd64.deb
RUN apt -y --fix-broken -f install

# Create a link so the python package can easily find the required binary
RUN ln -s /usr/local/bin/wkhtmltopdf /usr/bin/wkhtmltopdf
RUN pip install --break-system-packages docx2python pdfkit
