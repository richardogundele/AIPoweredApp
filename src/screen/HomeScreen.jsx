import React, {useEffect, useRef, useState} from 'react';
import {
  View,
  Text,
  SafeAreaView,
  TouchableOpacity,
  Image,
  ScrollView,
  Alert,
  StyleSheet,
  TextInput,
  PermissionsAndroid, Platform, ImageBackground
} from 'react-native';
import Voice from '@react-native-community/voice';
import {widthPercentageToDP as wp, heightPercentageToDP as hp} from 'react-native-responsive-screen';
import Icon from 'react-native-vector-icons/Ionicons';
import { useGetMessageQuery, useSendTextMutation } from '../redux/api';
import Tts from 'react-native-tts';
import { v4 as uuidv4 } from 'uuid';




const HomeScreen = () => {
  const [result, setResult] = useState('');
  const [recording, setRecording] = useState(false);

  const [inputText, setInputText] = useState('');
  const [messages, setMessages] = useState([]);
  const [responseText, setresponseText] = useState('')
 const {data, isLoading:loading, } = useGetMessageQuery()
 const [permissionGrated, setPermissionGrated] = useState(false)



useEffect(() => {
 if(data){
  if(data?.chat_history){
    // Assuming you have a state variable called 'messages' and 'setMessages' to manage the messages array

const updatedMessages = data?.chat_history?.map((messageItem) => {
  // Transform text_input into user message format
  const userMessage = {
    role: 'user',
    content: messageItem.text_input.trim(),
    id: new Date(),
  };

  // Transform message into assistant message format
  const assistantMessage = {
    role: 'assistant',
    content: messageItem.message,
    isPlaying: false,
    id: new Date(),
  };

  // Return both user and assistant messages
  return [userMessage, assistantMessage];
});

// Flatten the array to get a single array of messages
const flattenedMessages = updatedMessages.flat();

// Update the state with the new messages
setMessages(flattenedMessages);

  }
 }
}, [data])

  const scrollViewRef = useRef();
const [sendText, {isLoading}] =useSendTextMutation()

const updateScrollView = ()=>{
  setTimeout(()=>{
    scrollViewRef?.current?.scrollToEnd({ animated: true });
  },200)
}
  const speechStartHandler = e => {
    console.log('speech start event', e);
  };
  const speechEndHandler = e => {
    // setRecording(false);
    console.log('speech stop event', e);
  };
  const speechResultsHandler = e => {
    console.log('speech event: ',e);
    const text = e.value[0];
    setResult(text);
    
  };

  const speechErrorHandler = e=>{
    console.log('speech error: ',e);
  }
  const sendMessageVoice =async()=>{
    if(result.trim().length>0){
        let newMessages = [...messages];
        newMessages.push({role: 'user', content: result.trim(), id:new Date()});
        setMessages([...newMessages]);
       stopRecording()
       setResult('')
       updateScrollView()

       try {
        // Send the user's message to the server and await the response
        const response = await sendText(result.trim()).unwrap();
        if(response){
          setresponseText(response)
         }
        // Create a new array containing both the user message and the assistant's response
    
      } catch (error) {
        console.log(error);
      }
    }
  }

const sendMessageText = async () => {
  if (inputText.trim().length > 0) {
    // Create a user message object
    const userMessage = { role: 'user', content: inputText.trim() , id:new Date()};

    // Add the user message to the state and clear the input
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setInputText('');

    try {
      // Send the user's message to the server and await the response
      const response = await sendText(inputText).unwrap();
      if(response){
        setresponseText(response)
       }
      // Create a new array containing both the user message and the assistant's response
  
    } catch (error) {
      console.log(error);
    }
  }
};

  
  const startRecording = async () => {
   if(permissionGrated){
    setRecording(true);
 
    try {
      await Voice.start('en-GB'); // en-US

    } catch (error) {
      console.log('error', error);
    }
   }
   else{
    requestPermission()
   }
  };
  const stopRecording = async () => {
    
    setResult('')
    try {
      await Voice.stop();
      setRecording(false);
      speechEndHandler()
    } catch (error) {
      console.log('error', error);
    }
  };


  const requestPermission = async () => {
    try {
      if (Platform?.OS === 'android') {
        const granted = await PermissionsAndroid.request(
            PermissionsAndroid.PERMISSIONS.RECORD_AUDIO,
            {
              title: 'Permission to access photos',
              message: 'We need your permission to access your photos',
              buttonPositive: 'OK',
            }
          );
  
          if (granted === PermissionsAndroid.RESULTS.GRANTED) {
            console.log('Microphone permission granted');
            setPermissionGrated(true)
          } else {
            console.log('Microphone permission denied');
          }
      }
    } catch (err) {
      console.warn(err);
    }
  };

  useEffect(() => {

requestPermission()
  }, []); // Empty dependency array ensures this effect runs only once when the component mounts.


// console.log(messages, "messages")

  useEffect(() => {

    // voice handler events
    Voice.onSpeechStart = speechStartHandler;
    Voice.onSpeechEnd = speechEndHandler;
    Voice.onSpeechResults = speechResultsHandler;
    Voice.onSpeechError = speechErrorHandler;
    
    Tts.setDefaultLanguage('en-IE');
    Tts.addEventListener('tts-start', event => console.log('start', event));
    Tts.addEventListener('tts-finish', event => {console.log('finish', event)});
    Tts.addEventListener('tts-cancel', event => console.log('cancel', event));


    
    
    return () => {
        // Remove event listeners
        Voice.destroy().then(Voice.removeAllListeners);
      };
  }, []);

  useEffect(() => {
    if(responseText){
      const updatedMessages = [
        ...messages,
        { role: 'assistant', content: responseText, isPlaying:false, id:new Date() },
      ];
  
      // Update the state with the new array
      setMessages(updatedMessages);
      setresponseText('')
      updateScrollView();
  
    }
    }, [responseText])
    const startTextToSpeech = message => {
      if (message.content) {
        // Create a copy of the messages array with isPlaying set to false for all messages
        const updatedMessages = messages.map(msg => ({ ...msg, isPlaying: false }));
    
        // Update the state with the updated array to pause all previous messages
        setMessages(updatedMessages);
    
        // Find the index of the message to update
        const messageIndex = updatedMessages.findIndex(msg => msg.id === message.id);
    
        if (messageIndex !== -1) {
          // Update the isPlaying property of the specific message
          updatedMessages[messageIndex].isPlaying = true;
    
          // Update the state with the updated array to indicate the current message is playing
          setMessages(updatedMessages);
        }
    
        // Use the text-to-speech library's error callback to handle errors
        const n = message.content.split('\n').join(' ')
        Tts.getInitStatus().then(() => {
          Tts.speak(
            n,
            {
              iosVoiceId: 'com.apple.ttsbundle.Samantha-compact',
              rate: 0.5,
            }
        
          )
        });
       
      }
    };
    
    
    
  
    const stopSpeaking = (message)=>{
      if (message.content) {
        // Find the index of the message to update
        const messageIndex = messages.findIndex(m => m.id == message.id);
    
        if (messageIndex !== -1) {
          // Create a copy of the messages array
          const updatedMessages = [...messages];
    
          // Update the isPlaying property of the specific message
          updatedMessages[messageIndex].isPlaying = false;
    
          // Update the state with the updated array
          setMessages(updatedMessages);
        }
    
        // playing response with the voice id and voice speed
        Tts.stop();

      }
    }
  
  return (
    <View className="flex-1 bg-white">
  <SafeAreaView className="flex-1 flex ">
        {/* bot icon */}
        <View style={styles.header}>
      <Text style={styles.headerText}>ThespAIn</Text>
    </View>
    <View className=" flex-1 ">

   {
          messages.length>0 && (
             
        
              <View 
               
                className=" rounded-3xl p-4 flex-1">
                  <ScrollView  
                    ref={scrollViewRef} 
                    bounces={false} 
                    className="space-y-4" 
                    showsVerticalScrollIndicator={false}
                  >
                    {
                      messages.map((message, index)=>{
                        if(message.role=='assistant'){
                          if(message.content.includes('https')){
                            // result is an ai image
                            return (
                              <View key={index} className="flex-row justify-start">
                                <View 
                                  className="p-2 flex rounded-2xl bg-emerald-100 rounded-tl-none">
                                    <Image  
                                      source={{uri: message.content}} 
                                      className="rounded-2xl"  
                                      resizeMode="contain" 
                                      style={{height: wp(60), width: wp(60)}} 
                                    />
                                </View>
                              </View>
                              
                              
                            )
                          }else{
                            // chat gpt response
                            return (
                              <View key={index}> 
                                <View 
                                key={index} style={{width: wp(70)}} 
                                className="bg-emerald-100 p-2 text-black rounded-xl rounded-tl-none">
                                <Text className="text-neutral-800" style={{fontSize: wp(4)}}  >
                                  {message.content}
                                </Text>
                              </View>
                              <View className="flex flex-row my-3 items-center justify-between">
                              {
                                message?.isPlaying && message?.isPlaying ?   <TouchableOpacity onPress={()=> stopSpeaking(message)}>
                                <Icon name="pause-circle-outline" size={30} color="#000" />
                                </TouchableOpacity>:   <TouchableOpacity onPress={()=>startTextToSpeech(message)}>
                                <Icon name="play-circle-sharp" size={30} color="#000" />
                                </TouchableOpacity>
                              }
                              <View  
              className="w-[90%]" 
                              
                              >
                              <Image
                              className="w-full" 
              source={require('../../assets/images/voice.gif')}
              style={{ height: hp(4)}}
            />
                              </View>
                              </View>
                              </View>
                            )
                          }
                        }else{
                          // user input text
                          return (
                            <View key={index} className="flex-row justify-end">
                              <View 
                                style={{width: wp(70), backgroundColor:'#FFF', elevation:2}} 
                                className=" p-2 rounded-xl rounded-tr-none">
                                <Text className="text-black" style={{fontSize: wp(4)}}  >
                                  {message.content}
                                </Text>
                              </View>
                            </View>
                          );
                        }
                        
                        
                      })
                    }
                  </ScrollView>
              </View>
          )
        }


      
     
            </View>
        
        
        {/* recording, clear and stop buttons */}
     
       {
        recording ===false &&  <View className="mx-2" style={[styles.inputContainer, {height:wp(20)}]}>
        <TextInput
          style={styles.input}
          value={inputText}
          onChangeText={(text) => setInputText(text)}
          placeholder="Type your message..."
          className="text-black"
        />
        {
           isLoading ? <Image 
           source={require('../../assets/images/loading.gif')}
           style={{width: hp(5), height: hp(5), borderRadius:hp(6)}}
         /> : inputText.length >0  ?  <TouchableOpacity
            style={[styles.boxShadow, {
                width: hp(5), height: hp(5)
            }]}
            onPress={sendMessageText} 
            className="bg-white  rounded-full justify-center items-center flex"
          >
             <Icon name="send" size={25} color="#000" />
          </TouchableOpacity> :  <TouchableOpacity onPress={startRecording}>
            {/* recording start button */}
            <Image 
              className="rounded-full" 
              source={require('../../assets/images/recordingIcon.png')}
              style={{width: hp(8), height: hp(8)}}
            />
          </TouchableOpacity>
        }
      
      </View>
       }

       {
        recording &&    <View className="flex justify-center items-center">
        {
      
      <TouchableOpacity className="space-y-2">
      {/* recording stop button */}
      <Image 
        className="rounded-full" 
        source={require('../../assets/images/voiceLoading.gif')}
        style={{width: hp(10), height: hp(10)}}
      />
    </TouchableOpacity>
        }
       {
          isLoading ? <Image 
          className="  rounded-full justify-center items-center flex  absolute right-2 bottom-3"
          source={require('../../assets/images/loading.gif')}
          style={{width: hp(8), height: hp(8)}}
        />:   result && (
              <TouchableOpacity 
              style={styles.boxShadow}
              onPress={sendMessageVoice} 
              className="bg-white  rounded-full justify-center items-center flex w-14 h-14 absolute right-2 bottom-3"
            >
               <Icon name="send" size={30} color="#000" />
            </TouchableOpacity>
          )
        }
        {
          recording && (
            <TouchableOpacity 
              onPress={stopRecording} 
              className="bg-red-400 rounded-3xl p-2 absolute left-3"
            >
             <Icon name="stop-circle-outline" size={30} color="#fff" />
            </TouchableOpacity>
          )
        }
        
          
          
        
      </View>
       }
      </SafeAreaView>
   
   
    </View>
  );
};

export default HomeScreen;
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
   inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 1,
    paddingBottom: 1,
 
  },
  input: {
    flex: 1,
    backgroundColor: 'white',
    borderRadius: 20,
    paddingHorizontal: 10,
    borderWidth:1,
    borderColor:'grey',
    color:'#000'
  },
  header: {
    backgroundColor: '#fff',
    paddingVertical: 10,
    alignItems: 'center',
    elevation: 5, // Add elevation for box shadow
  },
  headerText: {
    fontSize: 24,
    color: '#000',
  },
  });
  