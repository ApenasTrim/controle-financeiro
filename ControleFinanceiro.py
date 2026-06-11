import PySimpleGUI as sg

sg.theme('DarkTeal12')

COR_VERDE  = '#00C853'
COR_VERMELHO = '#FF1744'
COR_FUNDO  = '#003E78'
COR_CARD   = '#012840'
COR_HEADER = '#003E78'
COR_TEXTO  = '#FFFFFF'
COR_BOTAO  = '#8C8C8C'

#guardador de transacao
transacoes = [] 

#calculo
def calcular_totais():
    entradas = sum(t['valor'] for t in transacoes if t['tipo'] == 'Entrada')
    saidas   = sum(t['valor'] for t in transacoes if t['tipo'] == 'Saída')
    total    = entradas - saidas
    return entradas, saidas, total

#converter
def converter_reais(valor):
    return f'R$ {valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')


def criar_janela():

    #cabecalho
    cabecalho = [
        [sg.Text('CONTROLE FINANCEIRO',
                 font=('Arial', 20, 'bold'),
                 text_color=COR_TEXTO,
                 background_color=COR_HEADER,
                 expand_x=True,
                 justification='center',
                 pad=(0, 15))]
    ]

   #resumo
    card_entradas = sg.Frame('Entradas', [
        [sg.Text(converter_reais(0),
                 key='-ENTRADAS-',
                 font=('Arial', 13, 'bold'),
                 text_color=COR_VERDE,
                 background_color=COR_CARD)]
    ], background_color=COR_CARD, title_color=COR_TEXTO, expand_x=True, pad=5)

    card_saidas = sg.Frame('Saidas', [
        [sg.Text(converter_reais(0),
                 key='-SAIDAS-',
                 font=('Arial', 13, 'bold'),
                 text_color=COR_VERMELHO,
                 background_color=COR_CARD)]
    ], background_color=COR_CARD, title_color=COR_TEXTO, expand_x=True, pad=5)

    card_total = sg.Frame('Total', [
        [sg.Text(converter_reais(0),
                 key='-TOTAL-',
                 font=('Arial', 13, 'bold'),
                 text_color=COR_TEXTO,
                 background_color=COR_CARD)]
    ], background_color=COR_CARD, title_color=COR_TEXTO, expand_x=True, pad=5)

    linha_cards = [card_entradas, card_saidas, card_total]

   #entrada
    formulario = [
        [
            sg.Column([[sg.Text('Descrição', background_color=COR_FUNDO, text_color=COR_TEXTO)],
                       [sg.Input(key='-DESC-', size=(20, 1))]],
                      background_color=COR_FUNDO),

            sg.Column([[sg.Text('Valor', background_color=COR_FUNDO, text_color=COR_TEXTO)],
                       [sg.Input(key='-VALOR-', size=(15, 1))]],
                      background_color=COR_FUNDO),

            sg.Column([[sg.Text('', background_color=COR_FUNDO)],   #espacador
                       [sg.Radio('Entrada', 'TIPO', key='-ENTRADA-', default=True,
                                 text_color=COR_TEXTO, background_color=COR_FUNDO),
                        sg.Radio('Saida', 'TIPO', key='-SAIDA-',
                                 text_color=COR_TEXTO, background_color=COR_FUNDO)]],
                      background_color=COR_FUNDO),

            sg.Column([[sg.Text('', background_color=COR_FUNDO)],
                       [sg.Button('ADCIONAR',
                                  button_color=(COR_TEXTO, COR_BOTAO),
                                  font=('Arial', 11, 'bold'),
                                  border_width=0,
                                  pad=(10, 0))]],
                      background_color=COR_FUNDO),
        ]
    ]

   #historico
    tabela = [
        [sg.Table(
            values=[],
            headings=['Descrição', 'Valor', 'Tipo'],
            col_widths=[25, 12, 10],
            auto_size_columns=False,
            justification='center',
            key='-TABELA-',
            expand_x=True,
            expand_y=True,
            background_color=COR_CARD,
            text_color=COR_TEXTO,
            header_background_color=COR_FUNDO,
            header_text_color=COR_TEXTO,
            alternating_row_color='#1C77BA',
            num_rows=10,
            row_height=25,
        )]
    ]

    #layout
    layout = [
        [sg.Column(cabecalho,
                   background_color=COR_FUNDO,
                   expand_x=True,
                   pad=(0, 0))],
        [sg.Column([linha_cards],
                   background_color=COR_FUNDO,
                   expand_x=True,
                   pad=(10, 10))],
        [sg.Column(formulario,
                   background_color=COR_FUNDO,
                   expand_x=True,
                   pad=(10, 5))],
        [sg.Column(tabela,
                   background_color=COR_FUNDO,
                   expand_x=True,
                   expand_y=True,
                   pad=(10, 10))],
    ]

    return sg.Window('Controle Financeiro',
                     layout,
                     size=(620, 520),
                     background_color=COR_FUNDO,
                     finalize=True)


#novos dados
def atualizar_janela(janela):
    entradas, saidas, total = calcular_totais()

    janela['-ENTRADAS-'].update(converter_reais(entradas))
    janela['-SAIDAS-'].update(converter_reais(saidas))
    janela['-TOTAL-'].update(converter_reais(total))

   #linhas
    linhas = [[t['descricao'], converter_reais(t['valor']), t['tipo']]
              for t in transacoes]
    janela['-TABELA-'].update(values=linhas)

#loop
janela = criar_janela()

while True:
    event, values = janela.read()

    #fechar
    if event == sg.WIN_CLOSED:
        break

    #adicionar
    if event == 'ADCIONAR':
        descricao = values['-DESC-'].strip()
        valor_str = values['-VALOR-'].strip()

        #aviso
        if not descricao:
            sg.popup('Preencha a descrição!', title='Aviso',
                     background_color=COR_FUNDO, text_color=COR_TEXTO)
            continue

        try:
            #virgula
            valor = float(valor_str.replace(',', '.'))
            if valor <= 0:
                raise ValueError
        except ValueError:
            sg.popup('Digite um valor numérico positivo!', title='Aviso',
                     background_color=COR_FUNDO, text_color=COR_TEXTO)
            continue

        tipo = 'Entrada' if values['-ENTRADA-'] else 'Saída'

        #adicionar a lista
        transacoes.append({'descricao': descricao, 'valor': valor, 'tipo': tipo})
        atualizar_janela(janela)

        #limpar
        janela['-DESC-'].update('')
        janela['-VALOR-'].update('')

janela.close()
