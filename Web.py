# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 20:20:14 2016

@author: Pedro
"""
import csv
import glob, os
from Bio import SearchIO
from ftplib import FTP 
from bioservices import UniProt
import re





class html:
    fname="index.html"
    conteudo=[]
    alinhamento=[]
    listaProt=[]
    protgene={}    
    session=""
    listaec=[]
    dictKegg={}
    #global ec_numberList
    #ec_numberList=[]
   

   #geneID=" "
    #procura=uniprot()

    def __init__(self):
         self.dicionario={}
         self.dicionarioProt={}
         self.titulo = "Trabalho Pratico de Laboratorios de BioInformatica 2015/16</br>Universidade do Minho"
         self.background = "bio2.jpg"
         self.u=UniProt()
         self.listaec=[]
        
#########################################################################       
        
    # UPLOAD PARA O SITE APENAS TEXTO    
    def upload_file(self,ficheiro):
        
        ftp = FTP('aquaeflavie.co.nf')  
        ftp.login('2034324_Laboratorios','bioinformatica2015') 
        print("local: "+ftp.pwd())
        ftp.cwd('/aquaeflavie.co.nf/')
        file = open(ficheiro,'rb') 
        ftp.storbinary('STOR '+ficheiro, file) 
        file.close()
        ftp.close()          
              
    #UPLOAD DO TEXTO PARA O SITE DIRECTAMENTE
    def upload_context(self):          
            
            yes = set(['yes','y', 'ye', ''])
            no = set(['no','n'])
            
            choice = input("Fazer Upload do \"contexto.txt\" para o servidor??").lower()
            if choice in yes:
               self.upload_file('contexto.txt')
               print("A fazer Upload")
            elif choice in no:
               print("Upload abortado")
            else:
               print("Responda com 'yes' or 'no'")
       

########################CARREGA DOS KEGGS#################################
               
   

    def parseKeggs(self,ficheiro):
        
        kegg_name = ficheiro 
        with open(kegg_name) as f:
            lines = f.read().splitlines()
        j=0
        
       
        ident=""        
        name=""
        product=""
        comment=""
        orthology=""
        title=""
        
        
        while j < len(lines):
            lines[j] = re.sub( '\s+', ' ', lines[j])
            
            if "TITLE" in lines[j]:
                title=lines[j].split("TITLE")[1]           
           
            if "ORTHOLOGY" in lines[j]:
                orthology=lines[j].split("ORTHOLOGY")[1]
           
            if "ENTRY" in lines[j]:
                ident=lines[j].split("ENTRY")[1]
              
            if "NAME" in lines[j]:
                name=lines[j].split("NAME")[1]
               
            if "PRODUCT" in lines[j]:
                product=lines[j].split("PRODUCT")[1] 
                           
            if "COMMENT" in lines[j]:
                comment=lines[j].split("COMMENT")[1] 
           
            if j>=0 and lines[j].startswith("//"):
                break
            j+=1
            
      
        self.dictKegg[ident]=[title,name,product,comment,orthology]

          

################### AUXILIARES ############################## 
 
    def muda_titulo(self,texto):
        self.titulo=texto
        return None
 
        
    def muda_fundo(self,texto):
        self.background=texto
        
         
############## CRIA O HTML TABELAS KEGGS ########################## 
 
    def parse_tableKegg(self):
            
            f=open("keggs_new.html","w")
            texto=[]
            texto.append('<html>\n')
            texto.append('<head><title>Keggs</title><link rel="stylesheet" href="mystyles.css"><meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head>\n')
            texto.append("<body>")
            texto.append('<div id="header">\n')
            texto.append('<H1>Kegg Results</H1>')
            texto.append('</div>') 
            texto.append("<body><div>\n") 
			 
            texto.append("<table border=\"1\" style=\"width:100%\">")   
            texto.append("<tr><th>ID</th><th>Title</th><th>Name</th><th>Product</th><th>Comment</th><th>Orthology</th></tr>")
           
            for file in glob.glob("Kegg\\*.txt"):
              self.parseKeggs(file)
            
            for key in self.dictKegg:
                texto.append("<tr><td>"+key+"</td><td>"+self.dictKegg[key][0]+"</td><td>"+self.dictKegg[key][1]+"</td><td>"+self.dictKegg[key][2]+"</td><td>"+self.dictKegg[key][3]+"</td><td>"+self.dictKegg[key][4]+"</td></tr>\n")
                 
            texto.append("</tr>\n")
           
            texto.append("</table>\n") 
            texto.append("</div>") 
            texto.append("</body></html>")
            f.writelines(texto)
            f.close()
            return None
      


################## CRIA OS FICHEIROS HTLM POR PROTEINA ###################        
   
   
    def parse_ListProteins(self):
            
            f=open("proteins.html","w")
            texto=[]
            texto.append('<!DOCTYPE html>\n')
            texto.append('<html>\n')
            texto.append('<head><title>Proteinas</title><link rel="stylesheet" href="mystyles.css"><meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head>\n')
            texto.append("<body>")
            texto.append('<div id="header">\n')
            texto.append('<H1>Lista de Proteinas</H1>')
            texto.append('</div>')
    

           
			 
            texto.append("<div>")
            texto.append("<table border=\"1\" style=\"width:100%\">")   
            texto.append("<tr><th>Assession Number</th><th>Locus Tag</th><th>Name</th><th>EC Number </th><th>Status</th></tr>")
           
          
          
           
            for file in glob.glob("Uniprot\\*.txt"):
                    fileBlast=("Blasts\\"+file.split('\\')[1].split('txt')[0][:-1]+".xml")
                    print("Teste1"+fileBlast)
                    SearchIO.convert(fileBlast, 'blast-xml', fileBlast[:-4]+'.tab', 'blast-tab', out_kwargs={'comments': False})                    
                    lista=self.parse_table(fileBlast[:-4]+'.tab')
                 
                    if lista[4] == None:
                        lista[4]="NA"
                    texto.append('<tr><td><p><a href=\"'+fileBlast[:-4]+'.html\">'+lista[0]+"</a></p></td><td>"+str(lista[1])+"</td><td>"+lista[3]+'</td><td><p><a href=\"keggs_new.html\">'+lista[4]+'</a></p></td><td>'+lista[2]+'</td></tr>\n')
              
               
                   
            texto.append("</table>\n") 
            texto.append("</div>") 
            texto.append("</body></html>")
            f.writelines(texto)
            f.close()
            return None
  
  
  
  
  
  
    def parse_table(self,nome_ficheiro):
                
            print("Nome do ficheito tab a ler"+nome_ficheiro)    
            retorno=[]    
            texto=[]
            f=open(nome_ficheiro,"r")
            reader = csv.reader(f, delimiter="\t")
            tablines = list(reader)
            html=open(nome_ficheiro[:-4]+".html","w")
            nomeP = os.path.basename(nome_ficheiro)[:-4]
            
           # texto.append("<h2>Features: </h2>" + str(self.dicionario[nomeP]) +"</p>")
            texto.append('<!DOCTYPE html>\n')
            texto.append('<html>\n')
            texto.append('<head><title>'+nomeP+'</title><link rel="stylesheet" href="mystyles.css"><link rel="stylesheet"  href="mystyles.css"><meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head>\n')
            texto.append("<body>")
            texto.append('<div id="header">\n')
            texto.append('<H1>'+nomeP+'</H1>')
            texto.append('</div>')
			  #texto.append("<hr>")
            texto.append("<div>")
            texto.append("<h4>Sequence:</h4>")
            #texto.append("<p>"+''.join(self.dicionario[nomeP].get("translation","NA")) +"</p>")
            
            texto.append("""<p align="justify">""")
            prot = ''.join(self.dicionario[nomeP].get("translation","NA"))
            i = 0
            for str1 in prot:
                if i==80:
                    texto.append("<br>")
                    i=0
                texto.append(str1)
                i+=1
            texto.append("</p>")
            
            
            texto.append("<hr>")
            texto.append("<h4>Gene ID:</h4>")
            texto.append("<ul>")            
            texto.append("<li>"+''.join(self.dicionario[nomeP]['db_xref'][1])+"</li>")
            texto.append("<li>Accession number NCBI: "+''.join(self.dicionario[nomeP]['accessionN'])+"</li>")
            retorno.append(self.dicionario[nomeP]['accessionN'])
            texto.append("<li>Locus tag: "+''.join(self.dicionario[nomeP]['locus_tag'])+"</li>")
            retorno.append(self.dicionario[nomeP]['locus_tag'])
            texto.append("<li>Gene Name: "+''.join(self.dicionario[nomeP]['geneName'])+"</li>")           
            texto.append("<li>Strand: "+''.join(self.dicionario[nomeP]['strand'])+"</li>")
            texto.append("</ul>")
            texto.append("<hr>")
            
            texto.append("<h4>Protein ID:</h4>")
            texto.append("<ul>")
           
            #texto.append("<li>Uniprot ID: "++"</li>")
            nome = ''.join(self.dicionario[nomeP]['uniprotID'])
                    
            an=''.join(self.dicionario[nomeP]['accessionN'])
       
            texto.append("<li>Uniprot ID:<a href=/Uniprot/"+an+".txt>"+nome+"</a></li>\n")
            texto.append("<li>Revision Status: "+''.join(self.dicionario[nomeP]['grauRevisao'])+"</li>")
            retorno.append(self.dicionario[nomeP]['grauRevisao'])
            texto.append("<li>Protein acession number: "+''.join(self.dicionario[nomeP]['accessionN'])+"</li>")
            texto.append("<li>Protein Name: "+''.join(self.dicionario[nomeP]['nomeProteina'])+"</li>")
            retorno.append(self.dicionario[nomeP]['nomeProteina'])
            texto.append("</ul>")
            texto.append("<hr>")
            texto.append("<h4>Protein Characteristics:</h4>")
            texto.append("<ul>")            
            texto.append("<li>AA number: "+''.join(self.dicionario[nomeP]['nAA'])+"</li>")
            texto.append("<li>Cellular Location: "+''.join(self.dicionario[nomeP]['subcellarLocation'])+"</li>")
            texto.append("<li>Function: "+''.join(self.dicionario[nomeP]['function'])+"</li>")
            texto.append("<li>GeneOntology Terms: "+''.join(self.dicionario[nomeP]['geneOnt'])+"</li>")
            texto.append("<li>EC_NUMBER: "+''.join(self.dicionario[nomeP]['ecNumber'])+"</li>")            
            retorno.append(self.dicionario[nomeP]['ecNumber'])
            texto.append("</ul>")
            texto.append("<hr>")
            texto.append("<h4>KeyWords:</h4>")
            texto.append("<p>"+''.join(self.dicionario[nomeP]['keyWords']) +"</p>")
        
            texto.append("<hr>")
            texto.append("<h4>Comments:</h4>")
            texto.append("<p>"+''.join(self.dicionario[nomeP]['mycomments'])+"</p>")
            texto.append("<hr>")  
            texto.append("</div>") 
            global blasts
            global passou
            if passou==False:
                passou=True    
                print("INDICE"+str(len(texto)))            
            texto.append("<div>")  
            blasts.append('<div class="titulo">Locus Tag: '+''.join(self.dicionario[nomeP]['locus_tag'])+'</div>')    
            blasts.append("<div>") 
            texto.append("<table border=\"1\" style=\"width:100%\">")  
            blasts.append("<table border=\"1\" style=\"width:100%\">") 
            texto.append("<tr><th>NCBI Link</th><th>Subject ID</th><th>%Identity</th><th>Align Len</th><th>Miss</th><th>gap</th><th>q.start</th><th>q.end</th><th>s.start</th><th>s.end</th><th>e.value</th><th>bit score</th></tr>")
            blasts.append("<tr><th>NCBI Link</th><th>Subject ID</th><th>%Identity</th><th>Align Len</th><th>Miss</th><th>gap</th><th>q.start</th><th>q.end</th><th>s.start</th><th>s.end</th><th>e.value</th><th>bit score</th></tr>")
           
           
            for linha in tablines:
                i=0
           
                texto.append("<td><p><a href=\"http://www.ncbi.nlm.nih.gov/protein/"+str(linha[1].split('|')[3])+"\">"+str(linha[1].split('|')[4])+"</a></p></td>\n")
                blasts.append("<td><p><a href=\"http://www.ncbi.nlm.nih.gov/protein/"+str(linha[1].split('|')[3])+"\">"+str(linha[1].split('|')[4])+"</a></p></td>\n")
                                
                for campo in linha:
                    if i!=0:                            
                        texto.append("<td>"+campo+"</td>\n")
                        blasts.append("<td>"+campo+"</td>\n")
                    i+=1
                texto.append("</tr>\n")    
                blasts.append("</tr>\n")    
            texto.append("</table>\n") 
            blasts.append("</table>\n") 
            texto.append("<div>") 
            blasts.append("<div>")
            texto.append("</body></html>")
            blasts.append("</body></html>")
            html.writelines(texto)
            html.close()
            f.close()
            print(retorno)
            return retorno
 




##############       PAGINA PRINCIPAL   #################################   
  
   
    def cria_html(self):
            
            global blasts
            blasts=[]
            global passou
            passou=False
            blasts.append('<!DOCTYPE html>\n')
            blasts.append('<html>\n')
            blasts.append('<head><title>UMBioBlastTool</title><link rel="stylesheet" href="mystyles.css"><link rel="stylesheet" type="text/css" href="mystyle.css"><meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head>\n')
            blasts.append('<style>')
            blasts.append('body{ background-image: url("'+ str(self.background) +'");background-repeat: repeat;}</style>')            
                     
            blasts.append('<body>\n')
            blasts.append('<div id="header">\n')
            blasts.append('<h1>BLASTS</h1>\n')
            blasts.append('</div>')
            blasts.append('</br>')
            
            
            self.conteudo.append('<!DOCTYPE html>\n')
            self.conteudo.append('<html>\n')
            self.conteudo.append('<head><title>UMBioBlastTool</title><link rel="stylesheet" href="mystyles.css"><link rel="stylesheet" type="text/css" href="mystyle.css"><meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head>\n')
            self.conteudo.append('<style>')
            self.conteudo.append('body{ background-image: url("'+ str(self.background) +'");background-repeat: repeat;}</style>')            
                     
            self.conteudo.append('<body>\n')
            self.conteudo.append('<div id="header">\n')
            self.conteudo.append('<h1>'+str(self.titulo)+'</h1>\n')
            
            
            self.conteudo.append('</div>\n') 
            
            
            self.conteudo.append('<div id="nav">\n')
            self.conteudo.append('<p><a href=\" https://github.com/Grupo4Bioinformatica/TrabalhoLaboratoriosBioinf.git"><h3>Project Source Code</h1></a></p>\n')
            self.conteudo.append('<p><a href=\"arvore.html"><h3>Gene Similarity Tree</h3></a></p>\n')
            self.conteudo.append('<p><a href=\"keggs_new.html"><h3>Kegg Results</h3></a></p>\n')            
            self.conteudo.append('<p><a href=\"proteins.html"><h3>Proteins</h3></a></p>\n')            
           # self.conteudo.append('<p><a href=\"genes.html"><h3>Genes</h3></a></p>\n')            
            self.conteudo.append('<p><a href=\"blasts.html"><h3>Blast Results</h3></a></p>\n')            
                      
            self.conteudo.append('</div>') 
            
            
            self.conteudo.append('<div id="section1">\n')
            self.conteudo.append('<h2><i>Treponema pallidum pallidum st.Nichols str</i></h2>\n') 
            self.conteudo.append('<h3>Genome Zone: 381901 - 501800</h3></br>\n')
            self.conteudo.append('<h3>GRUPO 4</h3>\n')
            self.conteudo.append('<p>\n')
            self.conteudo.append('Tiago Manuel Martinho Barbosa PG 19641 MBIO </br>\n')        
            self.conteudo.append('David Miguel Alves A53791 MIEI </br>\n')     
            self.conteudo.append('Pedro Duarte Cardoso Lopes A32652 MIEI </br>')  
            self.conteudo.append('Augusto Daniel Teixeira Moreira PG30381 MBIO</br>')  
            self.conteudo.append('</p>\n')
            self.conteudo.append('</div>')
            
            self.conteudo.append('<div id="abstract">\n')
            self.conteudo.append('<h3>Abstract</h3>\n')    
            self.conteudo.append('<?php\n')
            self.conteudo.append('echo file_get_contents("abstract.txt");')
            self.conteudo.append('?>')
            self.conteudo.append('</div>')
            
            self.conteudo.append('<div id="context">\n')
            self.conteudo.append('<h3>Context</h3>\n') 
            self.conteudo.append('<?php\n')
            self.conteudo.append('echo file_get_contents("contexto.txt");')
            self.conteudo.append('?>')
            self.conteudo.append('</div>')
            
            self.conteudo.append('<div id="footer">\n')
            self.conteudo.append('Universidade do Minho - Mestrado de BioInformática - 2015/16')
   
            
            self.parse_ListProteins()
            
            blasts.append('</body>\n')
            blasts.append('</html>\n')
            fb=open("blasts.html","w")
            fb.writelines(blasts)
            fb.close()
            self.conteudo.append('</body>\n')
            self.conteudo.append('</html>\n')
            return None

################################################################################
            
    def save_html(self):
            f=open(self.fname,"w")
            f.writelines(self.conteudo)
            f.close()
            return None
            
            
    def fazTudo(self):
            self.parse_tableKegg()
            self.cria_html()
            self.save_html()