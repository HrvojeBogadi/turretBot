import 'dart:convert';

import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'dart:math';

import 'package:flutter_mjpeg/flutter_mjpeg.dart';
import 'package:control_pad/control_pad.dart';
import 'package:http/http.dart' as http;


final String sendDataIP = "http://192.168.0.23";
final int sendDataPort = 8081;
final String stream = "http://192.168.0.23:8080/cam.mjpg";

void main() async{
  WidgetsFlutterBinding.ensureInitialized();

  SystemChrome.setPreferredOrientations([DeviceOrientation.landscapeRight])
    .then((value) => runApp(MyAppState()));

    print('Closing');
}

class MyAppState extends StatefulWidget{
  _MyApp createState() => _MyApp();
}

class _MyApp extends State<MyAppState>{
  bool isInTurretMode = false;
  double xLeft = 0, yLeft = 0, xRight = 0, yRight = 0;

  
  Future<http.Response> sendHTTPInfo() async{
    return await http.post(
      Uri.parse("$sendDataIP:$sendDataPort"),
      headers: 
        {
          'Content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        },
        body: "$xLeft:$yRight:$isInTurretMode"
    );
  }

  void onJoystickRightEvent(double angle, double distance){
    yRight = distance * cos(angle/(180) * pi);
    xRight = distance * sin(angle/(180) * pi);

    sendHTTPInfo();
    print("Right Joystick: X Cartesian: $xRight, Y Cartesian: $yRight");
  }

  void onJoystickLeftEvent(double angle, double distance){
    yLeft = distance * cos(angle/(180) * pi);
    xLeft = distance * sin(angle/(180) * pi);

    sendHTTPInfo();
    print("Left Joystick: X Cartesian: $xLeft, Y Cartesian: $yLeft");
  }

  void onButtonPress(){
    if (!isInTurretMode){
      print("Turret Mode Engaged!");
      isInTurretMode=true;
    }else{
      print("Turret Mode Disengaged!");
      isInTurretMode=false;
    }
    sendHTTPInfo();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Stack(
          fit: StackFit.expand,
          children: <Widget>[
            Container(
              color: Colors.blueGrey,
              child: Mjpeg(
                stream: stream, 
                isLive: true,
                fit: BoxFit.fill,
              )
            ),
            
            Container(
              alignment: AlignmentDirectional.bottomStart,
              child: Container(
                height: 125,
                width: 200,
                margin: EdgeInsets.only(left: 25, bottom: 5),
                child: JoystickView(
                  size: 125,
                  showArrows: false,
                  innerCircleColor: Colors.blueAccent,
                  backgroundColor: Colors.black87,
                  onDirectionChanged: onJoystickLeftEvent
                ),
              ),
            ),

            Container(
              alignment: AlignmentDirectional.bottomEnd,
              child: Container(
                height: 125,
                width: 200,
                margin: EdgeInsets.only(right: 25, bottom: 5),
                child: JoystickView(
                  size: 125,
                  showArrows: false,
                  innerCircleColor: Colors.blueAccent,
                  backgroundColor: Colors.black87,
                  onDirectionChanged: onJoystickRightEvent
                ),
              ),
            ),

            Container(
              alignment: AlignmentDirectional.bottomCenter,
              margin: EdgeInsets.only(bottom: 40),
              child: ElevatedButton(
                onPressed: onButtonPress,
                child: Text(
                  "Turret Mode"
                ),
                style: ElevatedButton.styleFrom(
                  primary: Colors.green,
                ),
              ),
            )
          ],
        ),
    );
  }

}