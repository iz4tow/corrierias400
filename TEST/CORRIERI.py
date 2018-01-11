# import the library
from appJar import gui

import jaydebeapi
import jpype

import time



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
##############################################FINE FILE INI IMPOSAZIONI###################################################################


##########################################################################################################################################
###########################################USCITA APPLICAZIONE CON CONTROLLO#########################################################
##########################################################################################################################################def checkStop(): 
def checkStop():
	return app.yesNoBox("USCITA", "Confermi di voler uscire?")
	#app.setStopFunction(checkStop)
##########################################################################################################################################
###########################################FINE USCITA APPLICAZIONE CON CONTROLLO#########################################################
##########################################################################################################################################


###############################################################################################################################
#####################################CONTROLLO CAMPI INSERITI##################################################################
###############################################################################################################################
def campi(): #FUNZIONE RICHIAMATA PER VALORIZZARE LE VARIABILI DAI CAMPI E CONTROLLARE CHE SIANO CORRETTI E PIENI
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
	
	codcli=app.getEntry("codicecliente").upper()
	if codcli=="":
		app.showLabel("avviso1")
		app.setLabel("avviso1","MANCA IL CAMPO -> CODICE CLIENTE")
		app.setLabelFg("avviso1", "red")#NOMELABEL, COLORE SFONDO
		errore_campi=1
		return
	if len(codcli)>6:
		errore_campi=1
		return
		
	codvettore=app.getEntry("codicevettore").upper()
	if codvettore=="":
		app.showLabel("avviso1")
		app.setLabel("avviso1","MANCA IL CAMPO -> CODICE VETTORE S72")
		app.setLabelFg("avviso1", "red")#NOMELABEL, COLORE SFONDO
		errore_campi=1
		return
		
	ragsocvettore=app.getEntry("ragsocvettore").upper()
	if ragsocvettore=="":
		app.showLabel("avviso1")
		app.setLabel("avviso1","MANCA IL CAMPO -> RAGIONE SOCIALE TRASPORTATORE")
		app.setLabelFg("avviso1", "red")#NOMELABEL, COLORE SFONDO
		errore_campi=1
		return
		
	indirizzo=app.getEntry("indirizzo").upper()
	if indirizzo=="":
		app.showLabel("avviso1")
		app.setLabel("avviso1","MANCA IL CAMPO -> indirizzo")
		app.setLabelFg("avviso1", "red")#NOMELABEL, COLORE SFONDO
		errore_campi=1
		return
		
	localita=app.getEntry("localita").upper()
	if localita=="":
		app.showLabel("avviso1")
		app.setLabel("avviso1","MANCA IL CAMPO -> LOCALITA")
		app.setLabelFg("avviso1", "red")#NOMELABEL, COLORE SFONDO
		errore_campi=1
		return
		
	provincia=app.getEntry("provincia").upper()
	if provincia=="":
		app.showLabel("avviso1")
		app.setLabel("avviso1","MANCA IL CAMPO -> PROVINCIA")
		app.setLabelFg("avviso1", "red")#NOMELABEL, COLORE SFONDO
		errore_campi=1
		return
	if len(provincia)!=2:
		app.showLabel("avviso1")
		app.setLabel("avviso1","CAMPO ERRATO -> PROVINCIA")
		app.setLabelFg("avviso1", "red")#NOMELABEL, COLORE SFONDO
		errore_campi=1
		return
	
	cap=app.getEntry("cap").upper()
	if cap=="":
		app.showLabel("avviso1")
		app.setLabel("avviso1","MANCA IL CAMPO -> C.A.P.")
		app.setLabelFg("avviso1", "red")#NOMELABEL, COLORE SFONDO
		errore_campi=1
		return
	if len(cap)!=5:
		app.showLabel("avviso1")
		app.setLabel("avviso1","CAMPO ERRATO -> CAP")
		app.setLabelFg("avviso1", "red")#NOMELABEL, COLORE SFONDO
		errore_campi=1
		return
		
	bartolini=app.getRadioButton("bartolini").upper()
	if bartolini=="":
		app.showLabel("avviso1")
		app.setLabel("avviso1","MANCA IL CAMPO -> BARTOLINI?")
		app.setLabelFg("avviso1", "red")#NOMELABEL, COLORE SFONDO
		errore_campi=1
		return
		
	magazzino=app.getRadioButton("magazzino").upper()
	if magazzino=="":
		app.showLabel("avviso1")
		app.setLabel("avviso1","MANCA IL CAMPO -> MAGAZZINO?")
		app.setLabelFg("avviso1", "red")#NOMELABEL, COLORE SFONDO
		errore_campi=1
		return
	if magazzino=="BORGHETTO":
		magazzino="BOR"
	if magazzino=="TREZZANO":
		magazzino="AUT"
	if magazzino=="TUTTI":
		magazzino="***"
	
	peso=app.getEntry("peso").upper()
	if peso=='':
		peso="999999"
	if len(peso)>6:
		app.showLabel("avviso1")
		app.setLabel("avviso1","CAMPO ERRATO -> PESO")
		app.setLabelFg("avviso1", "red")#NOMELABEL, COLORE SFONDO
		errore_campi=1
		return
		
	
	nazione=app.getEntry("nazione").upper()
	if len(nazione)!=2:
		app.showLabel("avviso1")
		app.setLabel("avviso1","CAMPO ERRATO -> NAZIONE")
		app.setLabelFg("avviso1", "red")#NOMELABEL, COLORE SFONDO
		errore_campi=1
		return
###############################################################################################################################
####################################FINE CONTROLLO CAMPI INSERITI@@@@@@@@@@@@##################################################
###############################################################################################################################

###########################################################################################################################
######################################DEFINIZIONE BOTTONI PREMUTI##########################################################
###########################################################################################################################
def press(button):
	app.hideLabel("avviso1") #nascondo avviso1 di comodo per avvisi
	app.hideLabel("avviso2") #nascondo avviso1 di comodo per avvisi

	data=time.strftime('%y%m%d')
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
	
	
###############################################################TASTO INSERISCI
	if button == "Inserisci":
		errore=0
		errore_campi=0
		campi()
		if errore_campi!=0:
			return
			
		curs.execute("SELECT * FROM CTEMELTST.TRTRA00F where TRCDEC='"+codvettore+"' AND TRCDTB='VET' AND TRCCOM='"+committente+"'")
		esiste=len(curs.fetchall())#lunghezza array estratto, conto le righe insomma...
		curs.execute("SELECT * FROM CTEMELTST.TXVET20F where VPCLIF='"+codcli+"'")
		esiste_cli=len(curs.fetchall())#lunghezza array estratto, conto le righe insomma...
		if esiste>0 or esiste_cli>0:
			app.showLabel("avviso1")
			app.setLabel("avviso1","RECORD DUPLICATO")
			app.setLabelFg("avviso1", "red")#NOMELABEL, COLORE SFONDO
		else:
			onetonintynine= range(1,99)
			for x in letter_range:
				for count in onetonintynine:
					elemento=count
					if elemento <10:
						elemento=x+'0'+str(elemento)
					else:
						elemento=x+str(elemento)
					curs.execute("SELECT * FROM CTEMELTST.TRTRA00F where TRCDEL='"+elemento+"' AND TRCDTB='VET' AND TRCCOM='"+committente+"'")
					esisteelemento=len(curs.fetchall())#lunghezza array estratto, conto le righe insomma...
					if esisteelemento<1:
						break
				if esisteelemento<1:
					break
			if errore==0:
				try:#INSERIMENTO IN TRTTRA00F
					curs.execute("INSERT INTO CTEMELTST.TRTRA00F (TRATR0,TRPFU0,TRDTC0,TRDTA0,TRCCOM,TRCDTB,TRCDEC,TRCDEL) VALUES (' ','"+utente+"','"+data+"','000000','"+committente+"','VET','"+codvettore+"','"+elemento+"')")
				except:
					errore=1
					app.showLabel("avviso1")
					app.setLabel("avviso1","!!!ERRORE INSERIMENTO IN TRTTRA00F - CONTATTARE CED!!!")
					app.setLabelFg("avviso1", "red")#NOMELABEL, COLORE SFONDO
			if errore==0:
				try:#INSERIMENTO IN BATRA00F
					curs.execute("INSERT INTO CTEMELTST.BATRA00F (BTATRC,BTCTRA,BTRAGS,BTRAGA,BTINDI,BTLOCA,BTPROV,BTCCAP,BTCNAZ,BTCFIS,BTPIVA,BTCBAN,BTCAGE,BTDAGE,BTCVAL,BTPFUT,BTDCRE,BTDAGG) VALUES ('','"+codvettore+"','"+ragsocvettore+"','','"+indirizzo+"','"+localita+"','"+provincia+"','"+cap+"','','.','','','','','','"+utente+"','20"+data+"','00000000')")
				except:
					errore=1
					app.showLabel("avviso1")
					app.setLabel("avviso1","!!!ERRORE INSERIMENTO IN BATRA00F - CONTATTARE CED!!!")
					app.setLabelFg("avviso1", "red")#NOMELABEL, COLORE SFONDO1
					print("INSERT INTO CTEMELTST.BATRA00F (BTATRC,BTCTRA,BTRAGS,BTRAGA,BTINDI,BTLOCA,BTPROV,BTCCAP,BTCNAZ,BTCFIS,BTPIVA,BTCBAN,BTCAGE,BTDAGE,BTCVAL,BTPFUT,BTDCRE,BTDAGG) VALUES ('','"+codvettore+"','"+ragsocvettore+"','','"+indirizzo+"','"+localita+"','"+provincia+"','"+cap+"','','.','','','','','','"+utente+"','20"+data+"','00000000')")
			if errore==0:
				try:#INSERIMENTO IN DIVET00F
					curs.execute("INSERT INTO CTEMELTST.DIVET00F (VEATRC,VECDVE,VEPRIO,VERAGS,VEINDI,VELOCA,VECDNZ,VECCAP,VEFCAP,VETELE,VERIFP,VENOTE,VECDTR,VETITR,VEDTCR,VEDTAG,VEPFUT,VENCON,VECODF,VEPIVA) VALUES ('','"+elemento+"','5','"+ragsocvettore+"','"+indirizzo+"','"+localita+"','','"+cap+"','','','','','"+codvettore+"','1','20"+data+"','00000000','"+utente+"','9999999','','')")
				except:
					errore=1
					app.showLabel("avviso1")
					app.setLabel("avviso1","!!!ERRORE INSERIMENTO IN DIVET00F - CONTATTARE CED!!!")
					app.setLabelFg("avviso1", "red")#NOMELABEL, COLORE SFONDO
					print("INSERT INTO CTEMELTST.DIVET00F (VEATRC,VECDVE,VEPRIO,VERAGS,VEINDI,VELOCA,VECDNZ,VECCAP,VEFCAP,VETELE,VERIFP,VENOTE,VECDTR,VETITR,VEDTCR,VEDTAG,VEPFUT,VENCON,VECODF,VEPIVA) VALUES ('','"+elemento+"','5','"+ragsocvettore+"','"+indirizzo+"','"+localita+"','','"+cap+"','','','','','"+codvettore+"','1','20"+data+"','00000000','"+utente+"','9999999','','')")
			if errore==0:
				try:#INSERIMENTO IN TXVET20F
					curs.execute("INSERT INTO CTEMELTST.TXVET20F (VPATRC,VPCCOM,VPCVET,VPPMAX,VPPFUT,VPDCRE,VPDAGG,VPCMAG,VPCLIF) VALUES ('','"+committente+"','"+elemento+"','"+peso+"','"+utente+"','20"+data+"','00000000','"+magazzino+"','"+codcli+"')")
				except:
					errore=1
					app.showLabel("avviso1")
					app.setLabel("avviso1","!!!ERRORE INSERIMENTO IN TXVET20F - CONTATTARE CED!!!")
					app.setLabelFg("avviso1", "red")#NOMELABEL, COLORE SFONDO
					print("INSERT INTO CTEMELTST.TXVET20F (VPATRC,VPCCOM,VPCVET,VPPMAX,VPPFUT,VPDCRE,VPDAGG,VPCMAG,VPCLIF) VALUES ('','"+committente+"','"+elemento+"','"+peso+"','"+utente+"','20"+data+"','00000000','"+magazzino+"','"+codcli+"')")
			
			##########SOLO BRT!!!!!!!
			if bartolini=="SI":
				try:#INSERIMENTO IN TRTAB00F
					curs.execute("INSERT INTO CTEMELTST.TRTAB00F (TBATRC,TBCDTB,TBCDEL,TBDETA,TBDTCR,TBDTAG,TBPFUT) VALUES ('','BRT','       "+elemento+"','"+ragsocvettore+"','"+data+"','000000','"+utente+"')")
				except:
					errore=1
			if errore==0:#FINALMENTE COMMITTIAMO TUTTO!
				curs.execute("commit")
				app.showLabel("avviso1")
				app.setLabel("avviso1","RECORD "+elemento+" INSERITO")
				app.setLabelFg("avviso1", "green")#NOMELABEL, COLORE SFONDO
			else:
				app.showLabel("avviso2")
				app.setLabel("avviso2","!!! ERRORE GRAVE SUL DATABASE !!!")
				app.setLabelFg("avviso2", "red")#NOMELABEL, COLORE SFONDO

				
###############################################################FINE TASTO INSERISCI			
			
			

###############################################################TASTO RICERCA		
			
	if button == "Ricerca":
		codcli=app.getEntry("codicecliente")
		curs.execute("SELECT e_mail FROM DBA.clienti_email where codice_cliente='"+codcli+"'")
		rows=curs.fetchall() 
		esiste=len(rows)
		if esiste>0:
			row=rows[0]
			email=row[0]
			app.setEntry("email",email)
		else:
			app.showLabel("avviso1")
			app.setLabel("avviso1","CLIENTE INESISTENTE")
			app.setLabelFg("avviso1", "red")#NOMELABEL, COLORE SFONDO
###############################################################FINE TASTO RICERCA


###############################################################TASTO ESCI
	if button == "Esci":
		if checkStop():
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
app.setLabelBg("title", "blue")#NOMELABEL, COLORE SFONDO
app.setLabelFg("title", "red") #NOME LABEL, COLORE CARATTERE


app.addLabel("cliente","Codice Cliente") #NOMELABEL, CONTENUTO
app.setLabelFg("cliente", "black")#NOMELABEL, COLORE SFONDO
app.addEntry("codicecliente")
app.setEntryDefault("codicecliente","Codice cliente")

app.addLabel("codvettore","Codice Vettore S72") #NOMELABEL, CONTENUTO
app.setLabelFg("codvettore", "black")#NOMELABEL, COLORE SFONDO
app.addEntry("codicevettore")
app.setEntryDefault("codicevettore","Codice Vettore da S72")

app.addLabel("vettore","Ragione Sociale Trasportatore") #NOMELABEL, CONTENUTO
app.setLabelFg("vettore", "black")#NOMELABEL, COLORE SFONDO
app.addEntry("ragsocvettore")
app.setEntryDefault("ragsocvettore","Ragione Sociale Trasportatore")

app.addLabel("ind","Indirizzo") #NOMELABEL, CONTENUTO
app.setLabelFg("ind", "black")#NOMELABEL, COLORE SFONDO
app.addEntry("indirizzo")
app.setEntryDefault("indirizzo","Indirizzo")

app.addLabel("loc","Località\Città") #NOMELABEL, CONTENUTO
app.setLabelFg("loc", "black")#NOMELABEL, COLORE SFONDO
app.addEntry("localita")
app.setEntryDefault("localita","Località\Città")

app.addLabel("prov","Provincia") #NOMELABEL, CONTENUTO
app.setLabelFg("prov", "black")#NOMELABEL, COLORE SFONDO
app.addEntry("provincia")
app.setEntryDefault("provincia","Provincia, es: MI")

app.addLabel("codpo","C.A.P.") #NOMELABEL, CONTENUTO
app.setLabelFg("codpo", "black")#NOMELABEL, COLORE SFONDO
app.addEntry("cap")
app.setEntryDefault("cap","CAP")

app.addLabel("naz","Sigla nazione") #NOMELABEL, CONTENUTO
app.setLabelFg("naz", "black")#NOMELABEL, COLORE SFONDO
app.addEntry("nazione")
app.setEntryDefault("nazione","IT")

app.addLabel("pes","Peso massimo in KG") #NOMELABEL, CONTENUTO
app.setLabelFg("pes", "black")#NOMELABEL, COLORE SFONDO
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


app.addButtons(["Inserisci","Ricerca","Esci"], press)


# start the GUI
app.go()

############################################################################################################################
###########################################FINE PARTE GRAFICA###############################################################
############################################################################################################################