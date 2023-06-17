import flet as ft
from flet import Page, AppBar, TextField, Image, FilledButton, Text, IconButton, Container


ranks = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "j", "q", "k"]
symbols = ["s"]

base = 'https://nftstorage.link/ipfs/bafybeif5ijkkxcnbvgjwckh5qxb3oznzoqi6qms7qg2yutmzhrz2i2flaa/'
imgs = [base+'back_gray.jpg', base+'back_red.jpg',
        base+'back_blue.jpg']

cardSrc = [base+'back_gray.jpg']

for s in symbols:
    for r in ranks:
        cardSrc.append(base+s + r + ".jpg")

payout = 1
balance = 100
bet = 1


def main(page: Page):


    def to_main():
        page.views.pop()
        page.go("/")

    def save_card(event):

        container = event.control
        imgIndex = cardSrc.index(container.content.src)


        to_main()

    def to_card_chooser(event):
        global payout
        container = event.control
        imgIndex = imgs.index(container.content.src)
        newImgIndex = (imgIndex - 1) % len(imgs)
        container.content.src = imgs[newImgIndex]

        if imgIndex == 0:
            payout *= 1.9
        elif newImgIndex == 0:
            payout /= 1.9
        payout = round(payout, 2)
        topBar[1] = ft.Text(f"payout: {payout}x", size=20, expand=True)
        page.go("/chooser")

    def route_change(route):
        if page.route == "/chooser":
            cardImgs = []
            for src in cardSrc:
                    cardImgs.append(Container(content=Image(src=src), on_click=save_card))

            page.views.append(
                ft.View(
                    "/chooser",
                    [
                        ft.Row(cardImgs, ft.MainAxisAlignment.SPACE_BETWEEN, wrap=True)
                    ],
                )
            )
        page.update()

    page.on_route_change = route_change

    topBar = [ft.Text(f"balance: {balance}$", size=20, expand=True),
              ft.Text(f"payout: {payout}x", size=20, expand=True),
              ft.Text(f"bet: {bet}$", size=20, expand=True)]

    icons = [Container(content=Image(src=imgs[0]), height=200, expand=True, on_click=lambda x: switchColor(x), on_long_press=to_card_chooser) for _ in range(5)]
    winners = [Container(content=Image(src=imgs[0]), height=200, expand=True) for _ in range(5)]

    def switchColor(event):
        global payout

        container = event.control
        imgIndex = imgs.index(container.content.src)
        newImgIndex = (imgIndex + 1) % len(imgs)
        container.content.src = imgs[newImgIndex]

        if imgIndex == 0:
            payout *= 1.9
        elif newImgIndex == 0:
            payout /= 1.9
        payout = round(payout, 2)
        topBar[1] = ft.Text(f"payout: {payout}x", size=20, expand=True)

        page.update()

    def removeDollar(event):
        global balance
        balance -= 1
        topBar[0] = ft.Text(f"balance: {balance}$", size=20, expand=True)
        page.update()


    unAddBtn = FilledButton(text="remove 1$", on_click=removeDollar)

    page.add(
        ft.Row(
            topBar,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Row(
            icons,
            ),
        ft.Row(
            winners,
            ),
        unAddBtn
    )


ft.app(target=main)
