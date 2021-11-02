#!/bin/python3

def activatesubprocesses(smtpusername):
    import subprocess

    print(smtpusername)
    try:
        process_output = open(BASE_DIR + "/scripts/subproccess.log", 'w')
    except Exception as e:
        print( 'Es konnte das subprocesslog : ' + str(BASE_DIR) + " /scripts/subproccess.log nicht erstellt werden")
        return False

    try:
         rc=subprocess.run(["/bin/python3",str(BASE_DIR) + "/emails/imap_sync.py",  smtpusername], capture_output=True)

    except Exception as e:
         print('Es konnte das subprocess : ' + str(BASE_DIR) + "/emails/imap_sync.py nicht gestartet werden")
         print(rc)
         return False


BASE_DIR='/home/verwaltung'
activatesubprocesses('brummel@beelze-solutions.de')
