from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from datetime import datetime, timedelta, time
from reservations.forms import BookForm
from reservations.models import Restaurant, Reservation


def home(request):
    return render(request, "home.html")


def restaurants_all(request):
    restaurants = Restaurant.objects.all()
    return render(request, "restaurants.html", {'restaurants': restaurants})



@login_required
def book_table(request, restaurant_id):
    if request.method == 'POST':
        form = BookForm(request.POST)
        form.restaurant_id = restaurant_id
        if form.is_valid():
            print(form.cleaned_data['date'], form.cleaned_data['time'], form.cleaned_data['number_of_people'])
            date = form.cleaned_data['date']
            time_from = form.cleaned_data['time']
            time_to = time(time_from.hour + 2, time_from.minute, time_from.second)
            datetime_from = datetime.combine(date, time_from)
            datetime_to = datetime.combine(date, time_to)
            people = form.cleaned_data['number_of_people']

            # Check date not in the past
            if date < datetime.today().date():
                form.add_error('date', 'Date cannot be in the past')
            else:
                restaurant = Restaurant.objects.get(pk=restaurant_id)
                # Check date and time in working hours
                if time_from < restaurant.opening_time:
                    form.add_error('time', 'Non working hours')
                else:
                    # Check capacity on date/time
                    bookings = Reservation.objects.filter(restaurant_id=restaurant_id, date=date).values()
                    time_to = restaurant.closing_time if restaurant.closing_time < time_to else time_to
                    occupied = 0
                    for b in bookings:
                        print(b)
                        if b['time'] >= time_from >= b['time_to'] or b['time'] >= time_to >= b['time_to']:
                            occupied += b.number_of_people
                    if occupied + people >= restaurant.capacity:
                        form.add_error('number_of_people', 'Not enough seats available')
                    else:
                        reservation = Reservation()
                        reservation.customer = request.user
                        reservation.restaurant = restaurant
                        reservation.date = date
                        reservation.time = time_from
                        reservation.time_to = time_to
                        reservation.number_of_people = people
                        reservation.save()

                        return render(request, "book_success.html", {'reservation': reservation})
    else:
        form = BookForm()
    return render(request, "book.html", {'form': form})


@login_required
def reservations_upcoming(request):
    reservations = Reservation.objects.filter(customer_id=request.user.id, date__gte=datetime.today().date())
    return render(request, "reservations_upcoming.html", {'reservations': reservations})


@login_required
def reservations_past(request):
    reservations = Reservation.objects.filter(customer_id=request.user.id, date__lte=datetime.today().date())
    return render(request, "reservations_past.html", {'reservations': reservations})


@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(restaurant__owner_id=request.user.id, date__gte=datetime.today().date())
    return render(request, "my_reservations.html", {'reservations': reservations})


@login_required
def reservations_cancel(request, rid):
    reservation = Reservation.objects.get(pk=rid)
    if reservation is not None:
        reservation.delete()
    return redirect('/reservations/upcoming')


@login_required
def my_restaurants(request):
    restaurants = Restaurant.objects.filter(owner_id=request.user.id)
    return render(request, "restaurants.html", {'restaurants': restaurants})
