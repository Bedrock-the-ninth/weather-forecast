from weather_forecast import OWMDataGrab
from email_handler import EmailDelivery


def main():
    data = OWMDataGrab()
    message = data.forcast_analysis()

    email_delivery = EmailDelivery(message=message)


if __name__ == "__main__":
    main()
