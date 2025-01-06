from datetime import datetime, timedelta

trainer_schedule = [{"date": datetime(2025, 1, 5).date(), "start_time": datetime(2025, 1, 5, 9, 0).time(), "end_time": datetime(2025, 1, 5, 17, 0).time()}]
bookings = [{"datetime_start": datetime(2025, 1, 5, 11, 0), "service_id": 1}, {"datetime_start": datetime(2025, 1, 5, 14, 0), "service_id": 1}, {"datetime_start": datetime(2025, 1, 5, 16, 30), "service_id": 1}]
cur_date = datetime(2025, 1, 5).date()
service_durations = {1: 60}

def bookings_times_discovery(trainer_schedule, bookings, cur_date, service_durations):
    schedule_times = []
    booking_intervals = []
    
    # 1. Raccogli gli orari del trainer per il giorno corrente
    for schedule in trainer_schedule:
        if schedule["date"] == cur_date:
            schedule_times.append((schedule["start_time"], schedule["end_time"]))

    # 2. Raccogli gli intervalli di prenotazione per il giorno corrente
    for booking in bookings:
        if booking["datetime_start"].date() == cur_date:
            service_id = booking["service_id"]
            if service_id not in service_durations:
                continue
            duration = timedelta(minutes=service_durations.get(service_id, 0))
            booking_intervals.append(
                (booking["datetime_start"].time(), (booking["datetime_start"] + duration).time())
            )

    # 3. Ordina gli intervalli di prenotazione
    booking_intervals.sort(key=lambda x: x[0])

    available_times = []

    # 4. Per ogni intervallo del trainer, trova gli spazi liberi
    for start_time, end_time in schedule_times:
        current_start = start_time
        for booking_start, booking_end in booking_intervals:
            # Se il booking inizia prima della disponibilità del trainer e finisce prima dell'orario disponibile
            if booking_start <= current_start < booking_end:
                current_start = booking_end
            elif current_start < booking_start <= end_time:
                # Se c'è uno spazio tra le prenotazioni
                available_times.append((current_start, booking_start))
                current_start = booking_end
        
        # Aggiungi l'ultimo intervallo libero se esiste
        if current_start < end_time:
            available_times.append((current_start, end_time))

    # 5. Se non ci sono spazi liberi, ritorna una lista vuota
    if not available_times:
        return []

    # Restituisci gli intervalli liberi come tuple (time, time)
    return available_times

# Esegui la funzione e stampa i risultati
print(bookings_times_discovery(trainer_schedule, bookings, cur_date, service_durations))
