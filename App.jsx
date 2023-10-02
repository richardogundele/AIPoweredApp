import {
  View,
  Text,
  SafeAreaView,
  TouchableOpacity,
  

  StyleSheet,
  TextInput,

} from 'react-native';
import React, { useEffect , useState} from 'react'
import HomeScreen from './src/screen/HomeScreen'
import { Provider } from 'react-redux'
import { store } from './src/redux/store'
import SplashScreen from './src/screen/SphashScreen'
import AsyncStorage from '@react-native-async-storage/async-storage';

import Login from './src/components/login';

const App = () => {
  const [isSplashVisible, setSplashVisible] = React.useState(true);
 const [LoggedIn,  setLoggedIn] = useState(false)

  useEffect(() => {
    // Simulate a splash screen duration (e.g., 3 seconds)
    const splashTimer = setTimeout(() => {
      setSplashVisible(false);
    }, 3000);

    return () => clearTimeout(splashTimer);
  }, []);
  useEffect(() => {
    // Check AsyncStorage for the email
    AsyncStorage.getItem('userEmail')
      .then((email) => {
        if (email) {
          // If email is found, user is logged in, so show HomeScreen
          setLoggedIn(true); // You'll need to manage a state for login status
        } else {
          // If email is not found, user is not logged in, so show login modal
          setLoggedIn(false);
        }
      })
      .catch((error) => {
        console.error('Error reading email from AsyncStorage:', error);
        // Handle error if necessary
      });
  }, []);

  return (
    <View className="flex-1">
      <Provider store={store}>
      {isSplashVisible ? (
        <SplashScreen />
      ) : (
       <>
       {
        LoggedIn ? <HomeScreen/> : 
       <Login setLoggedIn={setLoggedIn} />
       }
 
       
       </>
      )}
     

      </Provider>
    </View>
  )
}

export default App

const styles = StyleSheet.create({
  boxShadow:{
   shadowColor: "#000",
shadowOffset: {
 width: 0,
 height: 2,
},
shadowOpacity: 0.25,
shadowRadius: 3.84,

elevation: 3,
  },


 });