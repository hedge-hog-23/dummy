def send_email_with_text(body):
    import smtplib, ssl
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart

    sender_email = "senthilnaathankannappan@gmail.com"
    receiver_email = "malavika03@outlook.com"
    password = ""  # Replace with your actual 16-digit App Password

    message = MIMEMultipart("alternative")
    message["Subject"] = "Resume Matching Report"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Plaintext version
    part1 = MIMEText(body, "plain")

    # HTML version with CSS styling
    html = f"""\
    <html>
      <head>
        <style>
          body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f9f9f9;
            color: #333;
            padding: 20px;
          }}
          .container {{
            background-color: #ffffff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            max-width: 800px;
            margin: auto;
            white-space: pre-wrap;
          }}
          h2 {{
            color: #FFFFFF;
          }}
          code {{
            background: #f4f4f4;
            padding: 5px;
            border-radius: 4px;
            display: block;
          }}
        </style>
      </head>
      <body>
        <div class="container">
          <h2>Resume Matching Report</h2>
          <code>{body}</code>
          <p style="margin-top: 30px;">— Senthil</p>
        </div>
      </body>
    </html>
    """

    part2 = MIMEText(html, "html")

    # Attach both parts
    message.attach(part1)
    message.attach(part2)

    # Send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

    print("✅ Email sent successfully!")
