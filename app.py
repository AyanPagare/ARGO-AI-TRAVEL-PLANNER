import streamlit as st
import pandas as pd
import google.generativeai as genai
import base64
from datetime import date
import requests
from flight_search import search_flights
from dotenv import load_dotenv
import os


load_dotenv()

def get_best_prediction(train):

    predictions = []

    for seat in train["classAvailability"]:

        prediction = seat.get("prediction")

        if prediction:
            try:
                value=int(prediction.split('%')[0])
                predictions.append(value)
            except:
                    pass
    return max(predictions) if predictions else 0

def flight_duration_minutes(flight):

    duration = flight["duration"]

    hours = int(duration.split("h")[0])

    minutes = int(duration.split("h")[1].replace("m", "").strip())

    return hours * 60 + minutes
#if "current_page" not in st.session_state:
    #st.session_state.current_page = "home"
#if 'logged_in' not in st.session_state:
    #st.session_state.logged_in = False

#if 'page' not in st.session_state:
    #st.session_state.page = 'login'


#with open('Argo bg.png', 'rb') as image_file:
    #bg_image=base64.b64encode(image_file.read()).decode()

st.markdown('''
<style>


.stButton > button {
    width:100%;
    height:55px;
    background:#0D1B3D;
    color:white;
    border:none;
    border-radius:12px;
    font-size:18px;
    font-weight:600;
}

.stButton > button:hover {
    background:#1E3A8A;
}
.form-card{
    background:white;
    padding:30px;
    border-radius:20px;
    box-shadow:0px 8px 25px
rgba(0,0,0,0.08);
    border:1px solid #E5E7EB;
    
}


</style>
''', unsafe_allow_html=True)

st.markdown("""
<style>

/* Sidebar */
section[data-testid="stSidebar"]{
    background-color: #0F172A;
}

/* Sidebar text */
section[data-testid="stSidebar"] *{
    color: white;
}
div[role="radiogroup"] > label {
    background: #111827;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 8px;
}

div[role="radiogroup"] > label:hover {
    background: #1E293B;
}

</style>
""", unsafe_allow_html=True)

# ---------------- GEMINI SETUP ----------------

genai.configure(api_key=os.getenv('Gemini_API_Key'))
RAPIDAPI_KEY=os.getenv('RapidAPI_Key')

model = genai.GenerativeModel("gemini-2.5-flash")


# ---------------- LOAD DATA ----------------

try:
    df = pd.read_csv("travel_date.csv")
except:
    st.error("travel_date.csv not found")
    st.stop()

#if not st.session_state.logged_in:
    #st.image('ARGO Logo.png', width=250)
    #st.markdown('Welcome Back')
    #st.markdown('Login to continue your journey with ARGO')

    #email=st.text_input('Enter Your Email Address')
    #password=st.text_input('Enter Password', type='password')
    #col1, col2 = st.columns(2)

   # with col1:
        #if st.button('Login'):
            #if email and password:
                #st.session_state.logged_in = True
                #st.rerun()
            #else:
                #st.error('Please enter email id and password')

    #with col2:
        #if st.button('Sign Up'):
            
            #st.session_state.page = 'signup'
            #st.rerun()
            
    #if st.session_state.page == 'signup':
       # st.markdown('---')
        #st.markdown('Create Your Account')
        #name=st.text_input('Enter Your Name')
        #signup_email=st.text_input('Enter SignUp Email')
        #signup_password=st.text_input('Create Password', type='password')

        #if st.button('Create Account'):
            #if name and signup_email and signup_password:
                #st.success('Account Created Successfully!')
                #st.session_state.logged_in = True
                #st.rerun()
            #else:
                #st.error('Emty Fields Found')
    #st.stop()

station_codes = {
    'Dombivli' : 'KYN',
    'Mumbai' : 'CSMT',
    'Chennai' : 'MAS',
    'Tiruchirappalli' : 'TPJ',
    'Bangalore' : 'SBC',
    'Ahmedabad' : 'ADI',
    'Delhi' : 'NDLS',
    'Pune' : 'PUNE',
    'Hyderabad' : 'HYB',
    'Kolkata' : 'HWH',
    'Jaipur' : 'JP',
    'Amritsar' : 'ASR',
    'Coimbatore' : 'CBE',
    'Bhubaneswar' : 'BBS',
    'Lucknow' : 'LKO',
    'Patna': 'PNBE',
    'Goa': 'MAO',
    'Kochi': 'ERS',
    'Madurai': 'MDU',
    'Mangalore': 'MAJN',
    'Chandigarh': 'CDG',
    'Nagpur': 'NGP',
    'Nashik': 'NK',
    'Surat': 'ST',
    'Vadodara': 'BRC',
    'Visakhapatnam': 'VSKP',
    'Vijaywada': 'BZA',
    'Indore': 'INDB'
    }

def get_live_train_data(source_city, destination_city, travel_date):
    source_code=station_codes.get(source_city)
    destination_code=station_codes.get(destination_city)

    if not source_code or not destination_code:
        return None
    url = "https://irctc-api2.p.rapidapi.com/trainAvailability"

    querystring = {
        'source' : source_code,
        'destination' : destination_code,
        'date' : travel_date.strftime('%d-%m-%Y')
    }
    headers={
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': 'irctc-api2.p.rapidapi.com'

    }
    response=requests.get(
        url,
        headers=headers,
        params=querystring
    )
    return response.json()

# ---------------- UI ----------------

with st.sidebar:

    st.image("ARGO Logo rev.png", width=140)

    st.markdown('''
    <div style='
        background:#1E293B;
        padding:15px;
        border-radius:12px;
        margin-bottom:20px;
    '>
    <div>
        <h4 style='color:white;margin:0;'>👤Guest User</h4>
        <p style='color:#94A3B8;margin:0;'>Travel Planner</p>
    </div>

    </div>

    ''', unsafe_allow_html=True)

    st.markdown("### MAIN MENU")

    page = st.radio(
        "",
        [
            "✈️ Plan Journey",
            "🔖 Saved Trips",
            "❤️ Favorites",
            "🕒 Travel History"
        ],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown('ACCOUNT')
    st.button(" Profile", use_container_width=True)
    st.button(" Settings", use_container_width=True)
    st.markdown('---')
    if st.button('Logout'):
        st.session_state.logged_in = False
        st.session_state.page = 'login'
        st.success('Logged Out Successfully')
        st.rerun()
    st.markdown('''
    <div style='
        background:#1E293B;
        padding:15px;
        border-radius:12px;
        margin-bottom:20px;
    '>
    <div>
        <h4 style='color:white;margin:0;'>👑 Go Premium</h4>
        <p style='color:#94A3B8;margin:0;'>Unlock advanced features and smarter recommendations.</p>
        
    </div>

    </div>

    ''', unsafe_allow_html=True)
    premium = st.button('Upgrade Now', use_container_width=True)

    if premium:
        st.toast('Premium Coming Soon')

    

left_col, right_col = st.columns([1.2,1])
with left_col:


    st.image('ARGO Logo.png', width=220)
    st.markdown(
        ''' 
        <h1 style='color:#111827; font-size:32px;
        margin-bottom:30px;'>
        AI Route Guidance & Optimization
        </h1>
        
        <h4 style='color:#0F172A;'> Smart Route Optimization </h4>
        <p style='color:#374151; font-size:14px;'>
        Find the most efficient route </p>
        
        <h4 style='color:#0F172A;'>
        Budget-Conscious Travel </h4>
        <p style='color:#374151; font-size:14px;'>
        Save money with smart planning </p>
        
        <h4 style='color:#0F172A;'>
        Multi City Planning </h4>
        <p style='color:#374151; font-size:14px;'>
        Plan complex routes with ease
        </p>
        
        <h4 style='color:#0F172A;'> 
        AI Travel Recommendations </h4>
        <p style='color:#374151; font-size:14px;'>
        Get suggestions powered with AI
        </p>
        ''', unsafe_allow_html=True
    )
    
with right_col:
    all_cities=sorted(
        list(
            set(df['current_city']).union(
                set(df['destination'])

            )
        )
    )
    
    
    current_city = st.selectbox('Select Current City', all_cities)

    destination = st.selectbox('Select Destination', [city for city in all_cities if city != current_city])

    budget = st.number_input(
        "Enter Your Budget",
        min_value=0, step=500
    )

    travel_date = st.date_input('Select Travel Date', min_value=date.today())
    

    priority = st.selectbox(
        "Select Travel Priority",
        [
        "Cheapest",
        "Fastest",
        "Highest Confirmation"
        ]
    )
    generate = st.button(' ✈️ Generate Travel Plan', use_container_width=True)

    



# ---------------- BUTTON ----------------
def get_min_train_fare(train):
    fares = []

    for seat in train["classAvailability"]:
        fare=seat.get('fare')
        if fare is None:
            continue
        try:
            fares.append(int(str(fare).replace(',','').replace('Rs', '').strip()))
        except:
            pass
    return min(fares) if fares else float('inf')

    
if generate:
    
    flight_options=search_flights(
        current_city,
        destination,
        travel_date.strftime('%Y-%m-%d')
    )
    flight_options=[
        flight for flight in flight_options if flight['price']<=budget
    ]
    best_flight = None

    if flight_options:

        if priority == "Cheapest":

            best_flight = min(
                flight_options,
                key=lambda x: x["price"]
            )

        elif priority == "Fastest":

            

            best_flight = min(
                flight_options,
                key=flight_duration_minutes
            )

        elif priority == "Highest Confirmation":

        # Flights are considered confirmed bookings
            best_flight = flight_options[0]
        
    
    train_data = get_live_train_data(
        current_city,
        destination,
        travel_date
    )
    # st.write(train_data)
    best_train = None

    

    if train_data and train_data.get("success") and train_data.get("data"):

        trains = train_data["data"]

        if priority == "Cheapest":

            best_train = min(
                trains,
                key=get_min_train_fare
            )

        elif priority == "Fastest":

            best_train = min(
                trains,
                key=lambda x: x["duration"]
            )

        elif priority == "Highest Confirmation":
            best_train = max(
                trains,
                key=get_best_prediction
            )

    st.markdown('Recommendation Summary')

    if best_train and best_flight:
        train_fare=get_min_train_fare(best_train)
        if priority == 'Cheapest':
            winner=('Train' if train_fare<=best_flight['price'] else 'Flight')
        elif priority == 'Fastest':
            winner=('Train' if best_train['duration'] < flight_duration_minutes(best_flight) else 'Flight')
        else:
            winner=('Train' if get_best_prediction(best_train)>=100 else 'Flight')

        st.success(f"Recommemded Option: **{winner}**")

        if winner == 'Train':
            st.info(
                f'''
                Fits your selected priority: **{priority}**

                Starting Fare: Rs {get_min_train_fare(best_train)}

                Duration: {best_train['duration']}

                Best Confirmation: {get_best_prediction(best_train)} %
                '''

            )
        else:
            st.info(
                f'''
                Fits your selected priority: **{priority}**

                Flight Fare: Rs {best_flight['price']}

                Duration: {best_flight['duration']}

                Airline: {best_flight['airline']}

                '''
            )
    tab1, tab2, tab3= st.tabs(['Best Train Option', 'Best Flight Option', 'AI Advisor'])
    with tab1:
        if train_data and train_data.get('success') and train_data.get('data'):
            
            st.markdown('## Recommended Train')

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    'Train',


                 best_train['trainName']
                )
            with col2:
                st.metric(
                    'Duration',
                    best_train['duration']
                )
            with col3:
                st.metric('Rating',
                        str(best_train['rating'])
                )

            st.info(
                f'''
                {best_train['from']['name']}
                -->
                {best_train['to']['name']}

                Departure:
                {best_train['departure']}
                Arrival:
                {best_train['arrival']}
                Distance:
                {best_train['distanceKm']} km
                '''
            )
            st.markdown('### Available Classes')
            for seat in best_train['classAvailability']:
                st.success(
                    f'''
                    Class: {seat['class']}

                    Fare: Rs{seat['fare']}

                    Availability: {seat['availability']}

                    Prediction: {seat['prediction']}
                    '''
                )

            st.markdown('---')
            st.markdown('## Other Train Options')
            other_trains=[train for train in trains if train['trainNumber'] != best_train['trainNumber']]
            for train in other_trains[:4]:
                with st.container(border=True):
                    col1,col2,col3 = st.columns(3)

                    with col1:
                        st.metric(
                            'Train', 
                            train['trainName']
                        )
                    with col2:
                        st.metric(
                            'Duration',
                            train['duration']
                        )
                    with col3:
                        st.metric(
                            'Rating',
                            train['rating']
                        )
                    st.caption(
                        f'''
                        {train['from']['name']}
                        -->
                        {train['to']['name']}

                        Departure: {train['departure']}
                        Arrival: {train['arrival']}
                        '''
                    )
                    with st.expander('View Available Classes'):
                        for seat in train['classAvailability']:
                            st.write(
                                f'''
                                **Class:** {seat['class']}

                                **Fare:** Rs{seat['fare']}

                                **Availability:** {seat['availability']}

                                **Prediction:** {seat['prediction']}

                                '''
                            )
        else:
            st.error('No Train Data Founs')
            st.write(train_data)
    with tab2:

        if best_flight:

            st.markdown("## Best Flight")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Airline",
                    best_flight["airline"]
                )

            with col2:
                st.metric(
                    "Price",
                    f"₹{best_flight['price']}"
                )

            with col3:
                st.metric(
                    "Duration",
                    best_flight["duration"]
                )

            st.info(
                f"""
                From: {current_city}
                →
                To: {destination}

                Departure:
                    {best_flight['departure']}

                Arrival:
                    {best_flight['arrival']}
                """
            )
            st.markdown('---')
            st.markdown('Other Flight Options')

            other_flights=[flight for flight in flight_options if flight!=best_flight]

            for flight in other_flights[:4]:
                with st.container(border=True):
                    col1,col2,col3=st.columns(3)

                    with col1:
                        st.metric(
                            'Airline',
                            flight['airline']
                        )
                    with col2:
                        st.metric(
                            'Price',
                            f' Rs{flight['price']}'
                        )
                    with col3:
                        st.metric(
                            'Duration',
                            flight['duration']
                        )
                    
                    st.caption(f''' 
                               Departure: {flight['departure']}
                               Arrival: {flight['arrival']}
                               ''')

        else:

            st.warning("No flights found for this route.")  
    with tab3:

        prompt = f"""
        You are ARGO's AI Travel Advisor.

        Compare the following travel options and recommend ONLY ONE.

        Current City: {current_city}
        Destination: {destination}
        Travel Date: {travel_date}
        Budget: ₹{budget}
        User Priority: {priority}

        TRAIN DETAILS

        Train Name: {best_train['trainName'] if best_train else 'Not Available'}

        Duration: {best_train['duration'] if best_train else 'N/A'} minutes

        Minimum Fare: ₹{get_min_train_fare(best_train) if best_train else 'N/A'}
        
        Best Confirmation: {get_best_prediction(best_train) if best_train else 'N/A'}%

        FLIGHT DETAILS

        Airline: {best_flight['airline'] if best_flight else 'Not Available'}

        Duration: {best_flight['duration'] if best_flight else 'N/A'}

        Price: ₹{best_flight['price'] if best_flight else 'N/A'}

        Instructions:

        1. Recommend either Train or Flight.
        2. Explain WHY.
        3. Compare cost.
        4. Compare travel time.
        5. Compare reliability.
        6. Mention trade-offs.
        7. Give 3 practical travel tips.
        8. End with a one-line final recommendation.
        """

        response = model.generate_content(prompt)

        st.subheader("🤖 AI Travel Advisor")

        st.write(response.text)          
    
    

        # ---------------- GEMINI ----------------

        

total_routes = len(df)

all_cities = set(df["current_city"]).union(set(df["destination"]))
total_cities = len(all_cities)

st.markdown('---')
st.markdown(f"""
<div style='text-align:center;padding:20px;color:#6B7280;'>
            
<h4 style='color:#0F12A;'>ARGO AI Travel Planner v1.0</h4>
<p>
Supporting <b>{total_routes}+ Routes</b> Across
<b>{total_cities} Cities</b>
</p>

<p>
Designed & Developed by <b>Ayan Pagare</b><br>
NIT Trichy
</p>

</div>
""", unsafe_allow_html=True)