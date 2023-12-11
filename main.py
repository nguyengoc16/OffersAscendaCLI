
from handler import OfferFilter

def main():
    offer_filer = OfferFilter(path="input.json")

    my_offer = offer_filer.return_offer()

    print("--------------------")
    print(my_offer)

if __name__ == "__main__":
    main()