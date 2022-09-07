SELECT COALESCE(round(avg(datediff(accept_reject_date,proposed_date)),1),"None") FROM trade WHERE counterparty_email= %s and status<>"unaccepted" ', (session['email']),) 
    