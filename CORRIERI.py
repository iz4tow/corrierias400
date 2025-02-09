# import the library
from appJar import gui

import jaydebeapi
import jpype

import time

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders



#CONNESSIONE A DB2
jar = 'db2as400.jar' # location of the jdbc driver jar
args='-Djava.class.path=%s' % jar
jvm = jpype.getDefaultJVMPath()
jpype.startJVM(jvm, args)
conn=jaydebeapi.connect('com.ibm.as400.access.AS400JDBCDriver', 'jdbc:as400://10.1.12.80:50000',['QSECOFR','tony34']) #connessione al db2
curs=conn.cursor()
#########FINE DB2


##############################################APERTURA FILE INI IMPOSTAZIONI###############################################################
file = open("setting.ini", "r") 
for riga in file:
	if riga.find("|")!=-1: #SOLO LE RIGHE DELLE IMPOSTAZIONI CHE CONTENGONO IL | VENGONO CONSIDERATE, GLI ALTRI SONO COMMENTI
		riga=riga.replace(" ","") #TOGLO GLI SPAZI BIANCHI
		impostazione,valore=riga.split("|"); #PRENDE IMPOSTAZIONE E VALORE IMPOSTAZIONE USANDO COME SEPARATORE I :
		if impostazione=='committente':
			committente=valore
			committente=committente.replace("\n","")
		if impostazione=='utente':
			utente=valore
			utente=utente.replace("\n","")
		if impostazione=='letter_range':
			letter_range=valore
			letter_range=letter_range.replace("\n","")
		if impostazione=='contatto_interno':
			contatto_interno=valore
			contatto_interno=contatto_interno.replace("\n","")
		if impostazione=='mailuser':
			user=valore
			user=user.replace("\n","")
		if impostazione=='mailpassword':
			password=valore
			password=password.replace("\n","")
		if impostazione=='mail':
			fromaddr=valore
			fromaddr=fromaddr.replace("\n","")
##############################################FINE FILE INI IMPOSAZIONI###################################################################


##########################################################################################################################################
###########################################USCITA APPLICAZIONE CON CONTROLLO##############################################################
##########################################################################################################################################
def checkStop():
	return app.yesNoBox("USCITA", "Confermi di voler uscire?")
	#app.setStopFunction(checkStop)
##########################################################################################################################################
###########################################FINE USCITA APPLICAZIONE CON CONTROLLO#########################################################
##########################################################################################################################################

##########################################################################################################################################
###########################################MAIL RIEPILOGO A CONTATTO INTERNO##############################################################
##########################################################################################################################################
def mail_controllo():
	#RICHIAMO VARIABILI GLOBALI
	global contatto_interno
	global user
	global password
	global fromaddr
	
	global codcli
	global codvettore
	global ragsocvettore
	global localita
	global provincia
	global cap
	global bartolini
	global magazzino
	global indirizzo
	global nazione
	global errore_campi
	global peso
	global elemento
	
	oggi=time.strftime('%d-%m-%Y')#data di oggi formato DD-MM-YYYY
	fine=oggi #SALVO DIVERSA IMPOSTAZIONE NELLA BANDIERA LA FINE E' OGGI
	privacy = MIMEMultipart()
	privacy['From'] = fromaddr
	privacy['To'] = contatto_interno
	privacy['Subject'] = "INSERIMENTO CORRIERI SILOG"

	corpo="<h1>DATI CORRIERE INSERITI:</h1>"
	corpo=corpo+"CODICE CLIENTE: "+codcli+"<br>"
	corpo=corpo+"CODICE VETTORE S72: "+codvettore+"<br>"
	corpo=corpo+"RAGIONE SOCIALE: "+ragsocvettore+"<br>"
	corpo=corpo+"LOCALITA: "+localita+"<br>"
	corpo=corpo+"PROVINCIA: "+provincia+"<br>"
	corpo=corpo+"CAP: "+cap+"<br>"
	corpo=corpo+"INDIRIZZO: "+indirizzo+"<br>"
	corpo=corpo+"NAZIONE: "+nazione+"<br>"
	corpo=corpo+"PESO: "+peso+"<br>"
	corpo=corpo+"BARTOLINI: "+bartolini+"<br>"
	corpo=corpo+"MAGAZZINO: "+magazzino+"<br>"
	#corpo=corpo+"CODICE AS400: "+elemento+"\n"

	privacy.attach(MIMEText(corpo, 'html'))
	server = smtplib.SMTP('owa.melchioni.it', 25)
	server.starttls()
	server.login(user, password)
	privacyor = privacy.as_string()
	server.sendmail(fromaddr,contatto_interno, privacyor)
	server.quit()
##########################################################################################################################################
###########################################FINE MAIL RIEPILOGO A CONTATTO INTERNO#########################################################
##########################################################################################################################################


###############################################################################################################################
#####################################CONTROLLO CAMPI INSERITI##################################################################
###############################################################################################################################
def campi(): #FUNZIONE RICHIAMATA PER VALORIZZARE LE VARIABILI DAI CAMPI E CONTROLLARE CHE SIANO CORRETTI E PIENI
	#RICHIAMO VARIABILI GLOBALI
	global codcli
	global codvettore
	global ragsocvettore
	global localita
	global provincia
	global cap
	global bartolini
	global magazzino
	global indirizzo
	global nazione
	global errore_campi
	global peso
	
	#FINALMENTE I CAMPI!
	print("\n\n############################################################\n############################################################\nERRORI CAMPI:\n")
	codcli=app.getEntry("codicecliente").upper()
	if codcli=="":
		app.showLabel("avviso1")
		app.setLabel("avviso1","MANCA IL CAMPO -> CODICE CLIENTE")
		app.setLabelFg("avviso1", "red")
		print("MANCA IL CAMPO -> CODICE CLIENTE")
		errore_campi=1
	if len(codcli)>10:
			print("CAMPO ERRATO-> CODICE CLIENTE")#DEBUG CON CONSOLE ATTIVA
			errore_campi=1
		
	codvettore=app.getEntry("codicevettore").upper()
	if codvettore=="":
		app.showLabel("avviso1")
		app.setLabel("avviso1","MANCA IL CAMPO -> CODICE VETTORE S72")
		app.setLabelFg("avviso1", "red")
		print("MANCA IL CAMPO -> CODICE VETTORE S72")
		errore_campi=1
		if len(codcli)>6:
			print("CAMPO ERRATO -> CODICE VETTORE")#DEBUG CON CONSOLE ATTIVA
			errore_campi=1
		
	ragsocvettore=app.getEntry("ragsocvettore").upper()
	if ragsocvettore=="":
		app.showLabel("avviso1")
		app.setLabel("avviso1","MANCA IL CAMPO -> RAGIONE SOCIALE TRASPORTATORE")
		app.setLabelFg("avviso1", "red")
		print("MANCA IL CAMPO -> RAGIONE SOCIALE TRASPORTATORE")#DEBUG CON CONSOLE ATTIVA
		errore_campi=1
		
	indirizzo=app.getEntry("indirizzo").upper()
	if indirizzo=="":
		app.showLabel("avviso1")
		app.setLabel("avviso1","MANCA IL CAMPO -> indirizzo")
		app.setLabelFg("avviso1", "red")
		print("MANCA IL CAMPO -> INDIRIZZO")#DEBUG CON CONSOLE ATTIVA
		errore_campi=1
		
	localita=app.getEntry("localita").upper()
	if localita=="":
		app.showLabel("avviso1")
		app.setLabel("avviso1","MANCA IL CAMPO -> LOCALITA")
		app.setLabelFg("avviso1", "red")
		print("MANCA IL CAMPO -> LOCALITA")#DEBUG CON CONSOLE ATTIVA
		errore_campi=1
		
	provincia=app.getEntry("provincia").upper()
	if provincia=="":
		app.showLabel("avviso1")
		app.setLabel("avviso1","MANCA IL CAMPO -> PROVINCIA")
		app.setLabelFg("avviso1", "red")
		print("MANCA IL CAMPO -> PROVINCIA")#DEBUG CON CONSOLE ATTIVA
		errore_campi=1

	if len(provincia)!=2:#LA PROVINCIA E' SEMPRE LUNGA 2
		app.showLabel("avviso1")
		app.setLabel("avviso1","CAMPO ERRATO -> PROVINCIA")
		app.setLabelFg("avviso1", "red")
		print("ERRORE CAMPO -> PROVINCIA")#DEBUG CON CONSOLE ATTIVA
		errore_campi=1
	
	cap=app.getEntry("cap").upper()
	if cap=="":
		app.showLabel("avviso1")
		app.setLabel("avviso1","MANCA IL CAMPO -> C.A.P.")
		app.setLabelFg("avviso1", "red")
		print("MANCA IL CAMPO -> CAP")#DEBUG CON CONSOLE ATTIVA
		errore_campi=1

	if len(cap)!=5:#IL CAP E' SEMPRE LUNGO 5
		app.showLabel("avviso1")
		app.setLabel("avviso1","CAMPO ERRATO -> CAP")
		app.setLabelFg("avviso1", "red")
		print("ERRORE CAMPO -> CAP")#DEBUG CON CONSOLE ATTIVA
		errore_campi=1

		
	bartolini=app.getRadioButton("bartolini").upper()
	if bartolini=="":
		app.showLabel("avviso1")
		app.setLabel("avviso1","MANCA IL CAMPO -> BARTOLINI?")
		app.setLabelFg("avviso1", "red")
		print("MANCA IL CAMPO -> BARTOLINI")#DEBUG CON CONSOLE ATTIVA
		errore_campi=1

		
	magazzino=app.getRadioButton("magazzino").upper()
	if magazzino=="":
		app.showLabel("avviso1")
		app.setLabel("avviso1","MANCA IL CAMPO -> MAGAZZINO?")
		app.setLabelFg("avviso1", "red")
		print("MANCA IL CAMPO -> MAGAZZINO")#DEBUG CON CONSOLE ATTIVA
		errore_campi=1
	#CHE MAGAZZINO??
	if magazzino=="BORGHETTO":
		magazzino="BOR"
	if magazzino=="TREZZANO":
		magazzino="AUT"
	if magazzino=="TUTTI":
		magazzino="***"
	
	peso=app.getEntry("peso").upper()
	if peso=="":
		peso="9999999"#IL PESO DI DEFAULT E' 9999999 CIOE' IL MASSIMO
	if len(peso)>7:#CAMPO DI 7 POSIZIONI
		app.showLabel("avviso1")
		app.setLabel("avviso1","CAMPO ERRATO -> PESO")#DEBUG CON CONSOLE ATTIVA
		app.setLabelFg("avviso1", "red")
		print("ERRORE CAMPO -> PESO")#DEBUG CON CONSOLE ATTIVA
		errore_campi=1
		
	
	nazione=app.getEntry("nazione").upper()
	if len(nazione)>2:#LA NAZIONE E' MASSIMO 2, SE 0 SI SOTTINTENDE ITALIA
		app.showLabel("avviso1")
		app.setLabel("avviso1","CAMPO ERRATO -> NAZIONE")
		app.setLabelFg("avviso1", "red")
		print("MANCA IL CAMPO -> NAZIONE")#DEBUG CON CONSOLE ATTIVA
		errore_campi=1
		
	#####STAMPE PER INFO DEBUG SU CAMPI INSERITI
	print("\n\n############################################################\n############################################################\nINFO DEBUG CAMPI:")
	print("CODICE CLIENTE: "+codcli)
	print("CODICE VETTORE S72: "+codvettore)
	print("RAGIONE SOCIALE: "+ragsocvettore)
	print("LOCALITA: "+localita)
	print("PROVINCIA: "+provincia)
	print("CAP: "+cap)
	print("INDIRIZZO: "+indirizzo)
	print("NAZIONE: "+nazione)
	print("PESO: "+peso)
	print("BARTOLINI: "+bartolini)
	print("MAGAZZINO: "+magazzino)

###############################################################################################################################
####################################FINE CONTROLLO CAMPI INSERITI@@@@@@@@@@@@##################################################
###############################################################################################################################

###########################################################################################################################
######################################DEFINIZIONE BOTTONI PREMUTI##########################################################
###########################################################################################################################
def press(button):
	app.hideLabel("avviso1") #nascondo avviso1 di comodo per avvisi
	app.hideLabel("avviso2") #nascondo avviso1 di comodo per avvisi

	data=time.strftime('%y%m%d')#FORMATO AAMMDD
	
	#RICHIAMO VARIABILI GLOBALI
	global committente
	global utente
	global letter_range
	global codcli
	global codvettore
	global ragsocvettore
	global localita
	global provincia
	global cap
	global bartolini
	global magazzino
	global indirizzo
	global errore_campi
	global peso
	global elemento
	
	
###############################################################TASTO INSERISCI
	if button == "Inserisci":
		errore=0
		errore_campi=0
		esiste=0
		esiste_cli=0
		campi()
		if errore_campi!=0:#SE CI SONO ERRORI NEI CAMPI STAMPA DEBUG ED ESCE DALLA FUNZIONE, SICURAMENTE E' STATO UN ERRORE UTENTE
			print("ERRORE CAMPI!")
			return
			
		curs.execute("SELECT * FROM CTEGRPDAT.TRTRA00F where TRCDEC='"+codvettore+"' AND TRCDTB='VET' AND TRCCOM='"+committente+"'")
		esiste=len(curs.fetchall())#lunghezza array estratto, conto le righe insomma...
		curs.execute("SELECT * FROM CTEDATBOR.TXVET20F where VPCLIF='"+codcli+"' AND VPPMAX='"+peso+"'")
		esiste_cli=len(curs.fetchall())#lunghezza array estratto, conto le righe insomma...
		if esiste>0 or esiste_cli>0:#SE ESISTE IL CLIENTE+PESO O IL CORRIERE IN ANAGRAFICA
			if esiste>0 and esiste_cli>0:#SE ESISTONO ENTRAMBI
				app.showLabel("avviso1")
				app.setLabel("avviso1","Sembra sia già stato inserito da qualcun altro")
				app.setLabelFg("avviso1", "red")
			if esiste_cli<1:#SE ESISTE IL CORRIERE
				app.showLabel("avviso1")
				app.setLabel("avviso1","CORRIERE già esistente")
				app.setLabelFg("avviso1", "red")
			if esiste<1:#SE ESISTE SOLO LA COMBINAZIONE CLIENTE+PESO
				app.showLabel("avviso1")
				app.setLabel("avviso1","CLIENTE E PESO già associati")
				app.setLabelFg("avviso1", "red")
		else:
			#CICLO PER COSTRUIRE GLI "ELEMENTI" DEL TIPO A01,A02 PRENDENDO IL PRIMO LIBERO
			onetonintynine= range(1,99)
			for x in letter_range:
				for count in onetonintynine:
					elemento=count
					if elemento <10:
						elemento=x+'0'+str(elemento)
					else:
						elemento=x+str(elemento)
					curs.execute("SELECT * FROM CTEGRPDAT.TRTRA00F where TRCDEL='"+elemento+"' AND TRCDTB='VET' AND TRCCOM='"+committente+"'")
					esisteelemento=len(curs.fetchall())#lunghezza array estratto, conto le righe insomma...
					if esisteelemento<1:#SE E' LIBERO ROMPE IL CICLO...
						break
				if esisteelemento<1:#...E POI ESCE!
					break
			if errore==0:
				try:#INSERIMENTO IN TRTTRA00F
					curs.execute("INSERT INTO CTEGRPDAT.TRTRA00F (TRATR0,TRPFU0,TRDTC0,TRDTA0,TRCCOM,TRCDTB,TRCDEC,TRCDEL) VALUES (' ','"+utente+"','"+data+"','000000','"+committente+"','VET','"+codvettore+"','"+elemento+"')")
				except:
					errore=1
					app.showLabel("avviso1")
					app.setLabel("avviso1","!!!ERRORE INSERIMENTO IN TRTTRA00F - CONTATTARE CED!!!")
					app.setLabelFg("avviso1", "red")
					print("INSERT INTO CTEGRPDAT.TRTRA00F (TRATR0,TRPFU0,TRDTC0,TRDTA0,TRCCOM,TRCDTB,TRCDEC,TRCDEL) VALUES (' ','"+utente+"','"+data+"','000000','"+committente+"','VET','"+codvettore+"','"+elemento+"')")#DEBUG CON CONSOLE ATTIVA
			if errore==0:
				try:#INSERIMENTO IN BATRA00F
					curs.execute("INSERT INTO CTEDATBOR.BATRA00F (BTATRC,BTCTRA,BTRAGS,BTRAGA,BTINDI,BTLOCA,BTPROV,BTCCAP,BTCNAZ,BTCFIS,BTPIVA,BTCBAN,BTCAGE,BTDAGE,BTCVAL,BTPFUT,BTDCRE,BTDAGG) VALUES ('','"+codvettore+"','"+ragsocvettore+"','','"+indirizzo+"','"+localita+"','"+provincia+"','"+cap+"','','.','','','','','','"+utente+"','20"+data+"','00000000')")
				except:
					errore=1
					app.showLabel("avviso1")
					app.setLabel("avviso1","!!!ERRORE INSERIMENTO IN BATRA00F - CONTATTARE CED!!!")
					app.setLabelFg("avviso1", "red")
					print("INSERT INTO CTEDATBOR.BATRA00F (BTATRC,BTCTRA,BTRAGS,BTRAGA,BTINDI,BTLOCA,BTPROV,BTCCAP,BTCNAZ,BTCFIS,BTPIVA,BTCBAN,BTCAGE,BTDAGE,BTCVAL,BTPFUT,BTDCRE,BTDAGG) VALUES ('','"+codvettore+"','"+ragsocvettore+"','','"+indirizzo+"','"+localita+"','"+provincia+"','"+cap+"','','.','','','','','','"+utente+"','20"+data+"','00000000')")#DEBUG CON CONSOLE ATTIVA
			if errore==0:
				try:#INSERIMENTO IN DIVET00F
					curs.execute("INSERT INTO CTEDATBOR.DIVET00F (VEATRC,VECDVE,VEPRIO,VERAGS,VEINDI,VELOCA,VECDNZ,VECCAP,VEFCAP,VETELE,VERIFP,VENOTE,VECDTR,VETITR,VEDTCR,VEDTAG,VEPFUT,VENCON,VECODF,VEPIVA) VALUES ('','"+elemento+"','5','"+ragsocvettore+"','"+indirizzo+"','"+localita+"','','"+cap+"','','','','','"+codvettore+"','1','20"+data+"','00000000','"+utente+"','9999999','','')")
				except:
					errore=1
					app.showLabel("avviso1")
					app.setLabel("avviso1","!!!ERRORE INSERIMENTO IN DIVET00F - CONTATTARE CED!!!")
					app.setLabelFg("avviso1", "red")
					print("INSERT INTO CTEDATBOR.DIVET00F (VEATRC,VECDVE,VEPRIO,VERAGS,VEINDI,VELOCA,VECDNZ,VECCAP,VEFCAP,VETELE,VERIFP,VENOTE,VECDTR,VETITR,VEDTCR,VEDTAG,VEPFUT,VENCON,VECODF,VEPIVA) VALUES ('','"+elemento+"','5','"+ragsocvettore+"','"+indirizzo+"','"+localita+"','','"+cap+"','','','','','"+codvettore+"','1','20"+data+"','00000000','"+utente+"','9999999','','')")#DEBUG CON CONSOLE ATTIVA
			if errore==0:
				try:#INSERIMENTO IN TXVET20F
					curs.execute("INSERT INTO CTEDATBOR.TXVET20F (VPATRC,VPCCOM,VPCVET,VPPMAX,VPPFUT,VPDCRE,VPDAGG,VPCMAG,VPCLIF) VALUES ('','"+committente+"','"+elemento+"','"+peso+"','"+utente+"','20"+data+"','00000000','"+magazzino+"','"+codcli+"')")
				except:
					errore=1
					app.showLabel("avviso1")
					app.setLabel("avviso1","!!!ERRORE INSERIMENTO IN TXVET20F - CONTATTARE CED!!!")
					app.setLabelFg("avviso1", "red")
					print("INSERT INTO CTEDATBOR.TXVET20F (VPATRC,VPCCOM,VPCVET,VPPMAX,VPPFUT,VPDCRE,VPDAGG,VPCMAG,VPCLIF) VALUES ('','"+committente+"','"+elemento+"','"+peso+"','"+utente+"','20"+data+"','00000000','"+magazzino+"','"+codcli+"')")#DEBUG CON CONSOLE ATTIVA
			
			##########SOLO BRT!!!!!!!
			if bartolini=="SI":
				try:#INSERIMENTO IN TRTAB00F
					curs.execute("INSERT INTO CTEDATBOR.TRTAB00F (TBATRC,TBCDTB,TBCDEL,TBDETA,TBDTCR,TBDTAG,TBPFUT) VALUES ('','BRT','       "+elemento+"','"+ragsocvettore+"','"+data+"','000000','"+utente+"')")
				except:
					errore=1
			if errore==0:#FINALMENTE COMMITTIAMO TUTTO!
				curs.execute("commit")
				mail_controllo()#INVIO MAIL A OPERATORE
				app.showLabel("avviso1")
				app.setLabel("avviso1","RECORD "+elemento+" INSERITO")
				app.setLabelFg("avviso1", "green")
			else:
				app.showLabel("avviso2")
				app.setLabel("avviso2","!!! ERRORE GRAVE SUL DATABASE !!!")
				app.setLabelFg("avviso2", "red")

				
###############################################################FINE TASTO INSERISCI			
			
			

###############################################################TASTO RICERCA		
			
	if button == "Ricerca":
		campi() #POI NASCONDO GLI AVVISI DATO CHE è UNA RICERCA E NON DEVO CONTROLLARE I CAMPI
		app.hideLabel("avviso1") #nascondo avviso1 di comodo per avvisi
		app.hideLabel("avviso2") #nascondo avviso2 di comodo per avvisi
		
		###########RICERCA CORRIERE
		esiste=0
		if len(codvettore)>0:#CONTROLLO CHE SIA STATO INSERITO UN CODICE VETTORE
			curs.execute("SELECT TRCDEL FROM CTEGRPDAT.TRTRA00F where TRCDEC='"+codvettore+"'") #CERCO IL CODICE S72 SU TRTRA00F
			rows=curs.fetchall() 
			esiste=len(rows)
		if esiste>0:#SE ESISTE IL CORRIERE ESTRAGGO L'ANAGRAFICA ASSOCIATA
			elemento=str(rows[0][0])
			curs.execute("SELECT BTRAGS FROM CTEDATBOR.BATRA00F where BTCTRA='"+codvettore+"'") #CERCO IL CODICE S72 SU TRTRA00F
			rows=curs.fetchall() 
			ragsocvettore=str(rows[0][0])
			curs.execute("SELECT VPPMAX,VPCMAG FROM CTEDATBOR.TXVET20F where VPCVET='"+elemento+"'") #CERCO IL CODICE S72 SU TRTRA00F
			rows=curs.fetchall() 
			try:#PROVO PERCHE PESO POTREBBE NON ESSERCI E DARE ERRORE
				peso=str(rows[0][0]).replace(".0","")
			except:
				peso="9999999"
			try:#PROVO PERCHE MAGAZZINO POTREBBE NON ESSERCI E DARE ERRORE
				magazzino=str(rows[0][1])
			except:
				magazzino="***"
			elemento=elemento.strip()#VIA GLI SPAZI BIANCHI!!!
			curs.execute("SELECT TBCDTB FROM CTEDATBOR.TRTAB00F where TBCDEL='       "+elemento+"'") #CERCO elemento su tabella bartolini
			bartolini=curs.fetchall()
				
			#PARTE GRAFICA
			app.setEntry("ragsocvettore",ragsocvettore)
			app.setEntry("peso",peso)
			if magazzino=="BOR":
				app.setRadioButton("magazzino","BORGHETTO")
			if magazzino=="AUT":
				app.setRadioButton("magazzino","TREZZANO")
			if magazzino=="***":
				app.setRadioButton("magazzino","TUTTI")
			if len(bartolini)>0:
				app.setRadioButton("bartolini","SI")
			else:
				app.setRadioButton("bartolini","NO")
			app.showLabel("avviso1")
			app.setLabel("avviso1","CODICE ELEMENTO SILOG: "+elemento)
			app.setLabelFg("avviso1", "green")
		else:#SE NON ESISTE AVVISO1
			app.showLabel("avviso1")
			app.setLabel("avviso1","CORRIERE INESISTENTE")
			app.setLabelFg("avviso1", "red")
		
		
		###########RICERCA CLIENTE
		esiste=0
		if len(codcli)>0:#CONTROLLO CHE SIA STATO INSERITO UN CODICE CLIENTE
			curs.execute("SELECT DERAGS,DEINDI,DELOCA,DEPROV,DENAZI,DECAPC FROM CTEDATBOR.BADES00F where DECEXT='"+codcli+"'") #CERCO IL CODICE S72 SU TRTRA00F
			rows=curs.fetchall() 
			esiste=len(rows)
		if esiste>0:#SE ESISTE ESTRAGGO L'ANAGRAFICA ASSOCIATA DALLE VARIE TABELLE
			ragsoccliente=str(rows[0][0])
			indirizzo=str(rows[0][1])
			localita=str(rows[0][2])
			provincia=str(rows[0][3])
			nazione=str(rows[0][4])
			cap=str(rows[0][5])
			app.setEntry("indirizzo",indirizzo)
			app.setEntry("localita",localita)
			app.setEntry("provincia",provincia)
			app.setEntry("nazione",nazione)
			app.setEntry("cap",cap)

		else:#SE NON ESISTE AVVISO2
			app.showLabel("avviso1")
			app.setLabel("avviso2","CLIENTE INESISTENTE")
			app.setLabelFg("avviso2", "red")
			
			
###############################################################FINE TASTO RICERCA


###############################################################TASTO ESCI
	if button == "Esci":
		if checkStop():#FINESTRA CON ATTESA RISPOSTA
			app.stop()
###############################################################FINE TASTO ESCI


############################################################################################################################
###########################################FINE EVENTI BOTTONI##############################################################
############################################################################################################################			
			

			
			
############################################################################################################################
###########################################PARTE GRAFICA####################################################################
############################################################################################################################
# create a GUI variable called app
app = gui("INSERIMENTO CORRIERI SILOG - By FRANCO AVINO", "fullscreen")
app.setBg("yellow")
app.setFont(16)

# add & configure widgets - widgets get a name, to help referencing them later
app.addLabel("title", "\nINSERIMENTO CORRIERI SILOG\n") #NOMELABEL, CONTENUTO
app.setLabelBg("title", "blue")
app.setLabelFg("title", "red") #NOME LABEL, COLORE CARATTERE


app.addLabel("cliente","Codice Cliente") #NOMELABEL, CONTENUTO
app.setLabelFg("cliente", "black")
app.addEntry("codicecliente")
app.setEntryDefault("codicecliente","Codice cliente")

app.addLabel("codvettore","Codice Vettore S72") #NOMELABEL, CONTENUTO
app.setLabelFg("codvettore", "black")
app.addEntry("codicevettore")
app.setEntryDefault("codicevettore","Codice Vettore da S72")

app.addLabel("vettore","Descrizione Vettore") #NOMELABEL, CONTENUTO
app.setLabelFg("vettore", "black")
app.addEntry("ragsocvettore")
app.setEntryDefault("ragsocvettore","Ragione Sociale")

app.addLabel("ind","Indirizzo") #NOMELABEL, CONTENUTO
app.setLabelFg("ind", "black")
app.addEntry("indirizzo")
app.setEntryDefault("indirizzo","Indirizzo")

app.addLabel("loc","Località\Città") #NOMELABEL, CONTENUTO
app.setLabelFg("loc", "black")
app.addEntry("localita")
app.setEntryDefault("localita","Località\Città")

app.addLabel("prov","Provincia") #NOMELABEL, CONTENUTO
app.setLabelFg("prov", "black")
app.addEntry("provincia")
app.setEntryDefault("provincia","Provincia, es: MI")

app.addLabel("codpo","C.A.P.") #NOMELABEL, CONTENUTO
app.setLabelFg("codpo", "black")
app.addEntry("cap")
app.setEntryDefault("cap","CAP")

app.addLabel("naz","Sigla nazione") #NOMELABEL, CONTENUTO
app.setLabelFg("naz", "black")
app.addEntry("nazione")
app.setEntryDefault("nazione","IT")

app.addLabel("pes","Peso massimo in KG") #NOMELABEL, CONTENUTO
app.setLabelFg("pes", "black")
app.addEntry("peso")
app.setEntryDefault("peso","Peso")

app.addLabel("bart","Il corriere è Bartolini?") #NOMELABEL, CONTENUTO
app.addRadioButton("bartolini", "NO")
app.addRadioButton("bartolini", "SI")


app.addLabel("mag","Per quali magazzini è valido?") #NOMELABEL, CONTENUTO
app.addRadioButton("magazzino", "TUTTI")
app.addRadioButton("magazzino", "BORGHETTO")
app.addRadioButton("magazzino", "TREZZANO")

app.addLabel("avviso1"," ") #NOMELABEL, CONTENUTO
app.hideLabel("avviso1") #nascondo avviso1 di comodo per avvisi
app.addLabel("avviso2"," ") #NOMELABEL, CONTENUTO
app.hideLabel("avviso2") #nascondo avviso1 di comodo per avvisi


app.addButtons(["Inserisci","Ricerca","Esci"], press)#BOTTONI ASSOCIATI A FUNZIONE press


# start the GUI
app.go()

############################################################################################################################
###########################################FINE PARTE GRAFICA###############################################################
############################################################################################################################