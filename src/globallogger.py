import logging, queue
import logging.handlers
import utils

loggers = {}

def setup_custom_logger(name):   
    global loggers

    if loggers.get(name):
        return loggers.get(name)
    else:

        app_cfg = utils.get_app_config()
        formatter = logging.Formatter('%(asctime)s [%(module)s] %(levelname)s %(message)s')

        logger = logging.getLogger(name)
        #clean the handlers, otherwise you get duplicated records when logging
        if (logger.hasHandlers()):
            return logger
            #logger.handlers.clear()
        logger.propagate = False
        level = logging.getLevelName(utils.get_logging_level())    
        logger.setLevel(level)    
        log_queue     = queue.Queue()
        queue_handler = logging.handlers.QueueHandler(log_queue)       
        #set the non-blocking handler first
        logger.addHandler(queue_handler)

        # Stream is important for looking at the k8s pod logs.
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(formatter)
        
        # the local logging is fine, but there sould be a Fluent Bit integration, which sends logs to the central LMM instance
        timerotating_handler = logging.handlers.TimedRotatingFileHandler(utils.get_log_path().joinpath('app_rolling.log'), when='D', backupCount=30)
        timerotating_handler.setLevel(utils.get_logging_level())
        timerotating_handler.setFormatter(formatter)    

        ### email handler
        # TODO will be replaced by the central LMM service.
        # stream_log_to_email = app_cfg["stream_log_entries_to_email"]
        # if stream_log_to_email:
        #     email_secrets = utils.get_email_secrets()
        #     env = app_cfg["env"]
        #     application = app_cfg["application"]
        #     email_title = f"{env} - {application} - Log Record"
            
        #     smtp_server = email_secrets["smtp_server"]
        #     smtp_port = email_secrets["smtp_port"]

        #     email_from = email_secrets["monitoring"]["email_from"]
        #     email_to = email_secrets["monitoring"]["email_to"]
        #     email_user = email_secrets["monitoring"]["email_user"]
        #     email_password = email_secrets["monitoring"]["email_password"]
        
        #     smtp_handler = logging.handlers.SMTPHandler(
        #         mailhost=(smtp_server, smtp_port),
        #         fromaddr=email_from, 
        #         toaddrs=email_to,
        #         subject=email_title,
        #         credentials=(email_user, email_password),
        #         secure=() # pass an empty tuple
        #         )
        #     smtp_handler.setFormatter(formatter)
        #     smtp_handler.setLevel(logging.ERROR)
        #     #logger.addHandler(smtp_handler)
        
        #     listener = logging.handlers.QueueListener(log_queue, stream_handler, timerotating_handler, smtp_handler, respect_handler_level=True)
        # else:
        listener = logging.handlers.QueueListener(log_queue, stream_handler, timerotating_handler, respect_handler_level=True)
            
        listener.start()

    return logger