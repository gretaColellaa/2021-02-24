import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_grafo(self, e):
        m = self._view.dd_match.value
        try : int(m)
        except: self._view.create_alert("selezionare un match")

        self._model.creaGrafo(m)
        self._view.txt_result.controls.append(ft.Text(f"il grafo ha {self._model.getNumNodes()} nodi"
                                                      f" e {self._model.getNumEdges()} archi"))
        self._view.update_page()
    def handle_migliore(self, e):
        bestp, best = self._model.getBest()
        self._view.txt_result.controls.append(ft.Text(f"Il giocatore migliore è {bestp} con "
                                                      f"un delta efficienza complessivo di {best}"))
        self._view.update_page()

    def handle_simula(self, e):
        N = self._view.txt_azioni.value
        try: int(N)
        except: self._view.create_alert("Inserire un numero intero")
        teamh, teama = self._model.simula(N)

        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"il team {teamh[0]} ha segnato {teamh[1]} volte"
                                     f"con {teamh[2]} giocatori espulsi"))
        self._view.txt_result.controls.append(ft.Text(f"il team {teama[0]} ha segnato {teama[1]} volte"
                                     f"con {teama[2]} giocatori espulsi"))

        self._view.update_page()

    def fillDD(self):
        for m in sorted(self._model.getMatches()):
            self._view.dd_match.options.append(ft.dropdown.Option(
                text=m))
