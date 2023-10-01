from datetime import datetime
from app.db import execute_query, select_all, select_one

class Event():
    # @Description: Deze methode voegt het uitgegeven bedrag toe aan het uitje
    # @param: amount = bedrag dat is uitgegeven.
    # @param: eventId: Id van het uitje
    def addAmountToTotalAmount(amount: float, eventId: str) -> None:
        assert eventId is not None and eventId != ''
        query = "SELECT TotalAmount FROM Event WHERE eventId = %s"
        event = select_one(query, eventId)
        if event:
            newTotalAmount = event['TotalAmount'] + amount
            query = "UPDATE Event SET totalAmount = %s WHERE eventId = %s"
            execute_query(query, (newTotalAmount, eventId))
    
    # @Description: Deze methode voegt het betaalde bedrag toe aan het uitje, wat er is terug betaald door een deelnemer    
    # @param: expenditureId: Id van het betaalde betalingsverzoek, uit het betalingsverzoek kan ook het terug betaalde bedrag worden gehaald.
    def addAmountToPaidAmount(expenditureId: str) -> None:
        assert expenditureId is not None and expenditureId != ''
        query = """SELECT Event.PaidAmount AS paidAmount, Event.eventId, Expenditure.amount FROM Expenditure
                    JOIN ParticipantEvent ON Expenditure.participantEventId = ParticipantEvent.participantEventId
                    JOIN Event ON ParticipantEvent.eventId = Event.eventId
                    WHERE expenditureId = %s"""
        expenditure = select_one(query, expenditureId)
        if expenditure:
            newPaidAmount = expenditure['paidAmount'] + expenditure['amount']
            query = "UPDATE Event SET paidAmount = %s WHERE eventId = %s"
            execute_query(query, (newPaidAmount, expenditure['eventId']))
