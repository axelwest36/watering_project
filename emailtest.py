import smtplib
import ssl

port = 465
context = ssl.create_default_context()
sender_email = "schatjesplant@gmail.com"
# receiver_email = "victoria.plas@icloud.com"
receiver_email = "axel.westeinde@gmail.com"

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login(sender_email, "kamwyg-8Tuwtu-zudhom")
    message = """Subject: Plant heeft misschien dorst \n\n
        Hallo schat, \n\n
        Volgens mij is m'n reservoir bijna leeg. Kan je ff checken en deze bijvullen? Dankjewel! \n\n
        Groetjes, \n
        Je plant \n\n\n\n
        P.S. Please voorzichtig doen met alle kabeltjes en onderdelen, behalve het draadje van de waterpomp en de waterpomp zelf
        kan niks tegen water helaas :)
    """
    server.sendmail(sender_email, receiver_email, message)
