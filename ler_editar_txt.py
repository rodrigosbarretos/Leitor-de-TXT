import sys # Para conseguir manipular arquivos
import re # Para gerar padrões com expressões regulares
import os # Para manipulação de pastas e arquivos
import collections # Para ordenar dicionários
import pprint # Para imprimir 'bonitinho'

# Cria uma string que dará um nome diferente ao arquivo novo
# baseado no nome do arquivo original
# Caso não seja passado um nome/arquivo, ele terá como base
# o nome 'info.txt'
def nomeArquivoNovo(nomeAnterior,estilo="l"):
    temp = nomeAnterior.split("\\")[-1].split(".")
    return temp[0]+("_alterado." if estilo=='l' else "_grupo.")+temp[1]

def gerarLista(arquivo):
    listaNova = []

    for linha in arquivo:
        # Pegando cada linha do arquivo e dividindo em "palavras"
        # Essa divisão é feita toda vez que é encontrado um espaço
        valores = linha.split()
        for i in range(len(valores)):
            if valores[i]=="REG_SZ":
                #print(valores[i+1:])
                valor = " ".join(valores[i+1:])
                # Se NÃO houver a frase formada já inserida no textoNovo
                # então ela é adicionada no final da lista
                if not any(frase==valor for frase in listaNova): listaNova.append(valor)

    return sorted(listaNova, key=str.lower)

def filtrarGrupos(grupos):
    novoGrupos = grupos.copy()
    #arquivoTemp = open('log.txt','w')
    for grupo,lista in grupos.items():
        #arquivoTemp.write(grupo+": "+str(lista)+" --> "+str(len(lista))+"\n")
        if (not grupo=='?') and len(lista)==1:
            novoGrupos['?'].extend(lista)
            del novoGrupos[grupo]
    novoGrupos['?'] = sorted(novoGrupos['?'])
    return novoGrupos
    
def agrupar(lista):
    grupos = {'?':[]}
    padrao = re.compile(r'[A-Z,a-z]+')
    for linha in lista:
        palavra = linha.split()[0].upper()
        palavra = palavra if not (palavra=='THE' or not padrao.search(palavra)) else '?'
        #print(palavra)
        if not grupos.setdefault(palavra,[linha]) == [linha]:
            grupos[palavra].append(linha)
    
    return filtrarGrupos(grupos)
    
def formatarTXT(args):
    # Caso não seja passado um nome/arquivo, ele terá como base
    # o nome "info.txt"
    nomeDoArquivo = args[1] if len(args) > 1 else "info.txt"
    
    arquivo = open(nomeDoArquivo,"r") # Abrindo aquivo em modo de leitura

    textoNovo = gerarLista(arquivo)

    #for linha in textoNovo: # Imprimindo resultado na tela
    #    print("- "+linha)

    arquivo.close() # Fechando o arquivo original

    arquivo2 = open(nomeArquivoNovo(nomeDoArquivo),"w") # Criando o arquivo novo
    for linha in textoNovo: # Escrevendo no arquivo novo
        arquivo2.write("- "+linha+"\n")

    arquivo2.close()
    
    textoNovoAgrupado = agrupar(textoNovo)
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(agrupar(textoNovo))
    
    arquivo3 = open(nomeArquivoNovo(nomeDoArquivo,"g"),"w") # Criando o arquivo novo
    for grupo,linhas in textoNovoAgrupado.items(): # Escrevendo no arquivo novo
        if grupo=='?':
            for linha in linhas:
                arquivo3.write("- "+linha+"\n")
        else:
            arquivo3.write("\n=== "+grupo+" ===\n")
            for linha in linhas:
                arquivo3.write("- "+linha+"\n")

    arquivo3.close()

# Se esse arquivo for usado como principal, irá executar o comando do
# IF. Caso contrário não fará nada
if __name__ == "__main__":
    formatarTXT(sys.argv)

def test_listaFinal():
    assert gerarLista(open("teste.txt","r")) == ["Corel Graphics - Windows Shell Extension 32 Bit Keys",
                                       "Microsoft Visual C++ 2015 x64 Minimum Runtime - 14.0.24210",
                                       "Microsoft Visual Studio Tools for Applications 2012 x64 ???? - ???????",
                                       "SAMSUNG USB Driver for Mobile Phones",
                                       "Windows Live ID Sign-in Assistant"]
