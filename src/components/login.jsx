import { StyleSheet, Text, View, TextInput, TouchableOpacity } from 'react-native'
import React, { useEffect, useState } from 'react'
import { useRegisterMutation } from '../redux/api'
import {widthPercentageToDP as wp, heightPercentageToDP as hp} from 'react-native-responsive-screen';
import AsyncStorage from '@react-native-async-storage/async-storage';

const Login = ({setLoggedIn}) => {
    const [register, {isLoading}]= useRegisterMutation()
    const [isError, setIsError] = useState('')
    const [email, setEmail] = useState('')
    const sendRegister = async () => {

        const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$/;
     if (!email) {
          setIsError('email is required.');

        } else if (!emailPattern.test(email)) {
          setIsError('invalid email format.');
        }
        else {
          // Create a user message object
        
      
          try {
            
            const response = await register(email).unwrap();
            console.log(response)
            if(response){
             setLoggedIn(true)
             AsyncStorage.setItem('userEmail', email)
             }
            // Create a new array containing both the user message and the assistant's response
        
          } catch (error) {
            console.log(error);
            setIsError('something went wrong')
          }
        }
      };
    
    useEffect(() => {
   if(isError){
    setTimeout(() => {
        setIsError('')
    }, 2000);
   }
    }, [])
    
  return (
    <View  className="flex-1 px-5 bg-white justify-center items-center">
    <TextInput
   style={[styles.input, {
     height:hp(8),
     width:'100%'
   }]}
   placeholder="Email"
   onChangeText={(text) => setEmail(text)}
 />
<View className="mt-10 w-full justify-center items-center">
<View className="w-full justify-center items-center">
<Text className="text-red-700 text-xs">{isError}</Text>
 </View>
 <TouchableOpacity
   style={[styles.loginButton, {width:'70%', height:hp(7)}]}
   className=" flex justify-center items-center"
   onPress={sendRegister}
 >
   <Text style={[styles.loginButtonText, {fontSize:wp(5)}]}>{isLoading ?'processing...':'Get Started'}</Text>
 </TouchableOpacity>
</View>
</View>
  )
}

export default Login

const styles = StyleSheet.create({
    input: {
        backgroundColor: 'white',
        borderRadius: 20,
        paddingHorizontal: 10,
        borderWidth:1,
        borderColor:'#87CEEB',
        color:'#000'
      },
      loginButton: {
       backgroundColor: '#87CEEB',
       padding: 10,
       borderRadius: 5,
       alignItems: 'center',
     },
     loginButtonText: {
       color: 'white',
     },
})