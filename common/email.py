import os
import smtplib
import zipfile
from email.mime.text import MIMEText  # 正文用
from email.header import Header  # 标题用
from email.mime.multipart import MIMEMultipart
from common import log
from common import utils

class SendEmail:

    def __init__(self):
        self.Log = log.Mylog()
        #初始化email参数
        data = utils.readyaml(f_name='D:/pythonProject/config/galbalsetting')
        self.attachment_name = data['email']['Attachment_name'] #邮件标题
        self.send_addr = data['email']['sender']
        self.send_passwd = data['email']['send_pwd']
        self.receive_addr = data['email']['receivers']
        self.dirpath = data['email']['send_file_path']
        self.receive_email_port = data['email']['receive_email_port']
        self.email_content = data['email']['email_content']
        #压缩文件参数
        self.zip_file = data['email']['zip_file_path']

    def send_email(self):
        # 构造邮件：
        theme = MIMEMultipart()
        theme['From'] = self.send_addr  # 发件人
        theme['To'] = self.receive_addr  # 收件人的名字
        theme['Subject'] = Header(self.attachment_name, 'utf-8').encode()  # u一般用在中文字符串前面，防止因为源码储存格式问题
        #邮件正文
        theme.attach(MIMEText(self.email_content,'plain','utf-8'))
        # 发送的附件内容
        msg = MIMEText(open(self.dirpath, 'rb').read(), "base64", "utf-8")
        msg['Content-Type'] = 'application/octet-stream'
        msg["Content-Disposition"] = 'attachment; filename=' + self.dirpath

        try:
            # 实例化一个邮箱
            smtp = smtplib.SMTP()
            smtp.connect(host='smtp.163.com', port=self.receive_email_port)  # 这是发送出去的邮箱的smtp的地址和默认端口
            smtp.login(self.send_addr, self.send_passwd)  # 这是登录的账号和smtp密码，用于除了网页以外的客户端登录
            # 发送邮件，传入发送账号，接收账号，将from和to subject当做字符串传入
            smtp.sendmail(self.send_addr,self.receive_addr, msg.as_string())
            smtp.quit()  # 关闭连接
            self.Log.info('success:邮件发送成功！')
        except smtplib.SMTPException:
            self.Log.error('error:邮件发送失败！')

    def zipDir(self):
        zip = zipfile.ZipFile(self.zip_file, "w", zipfile.ZIP_DEFLATED)
        try:
            for path, dirnames, filenames in os.walk(self.zip_file):
                # 去掉目标跟路径，只对目标文件夹下边的文件及文件夹进行压缩
                fpath = path.replace(self.zip_file, '')

                for filename in filenames:
                    zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
            zip.close()
            self.Log.info('success:文件压缩成功！')
        except Exception as e:
            self.Log.error('error:文件压缩失败！错误信息：{}'.format(e))


if __name__ == '__main__':
    em = SendEmail()
    em.zipDir()