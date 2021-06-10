import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'dart:math';
import 'dart:io';
import 'dart:async';

import 'package:flutter_mjpeg/flutter_mjpeg.dart';

import 'package:control_pad/control_pad.dart';


final String url = "192.168.0.23";

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
  double xLeft, yLeft, xRight, yRight = 0;
  double resWidth = 1200;
  double resHeight = 480;
  String stream = "http://192.168.0.23:8080/cam.mjpg";
  
  void onJoystickRightEvent(double angle, double distance){
    yRight = distance * cos(angle/(180) * pi);
    xRight = distance * sin(angle/(180) * pi);

    print("Right Joystick: X Cartesian: $xRight, Y Cartesian: $yRight");
    //socket.write("Right Joystick Position:$yRight");
  }

  void onJoystickLeftEvent(double angle, double distance){
    yLeft = distance * cos(angle/(180) * pi);
    xLeft = distance * sin(angle/(180) * pi);

    print("Left Joystick: X Cartesian: $xLeft, Y Cartesian: $yLeft");
    //socket.write("Right Joystick Position:$xLeft");
  }

  void onButtonPress(){
    if (!isInTurretMode){
      print("Turret Mode Engaged!");
      isInTurretMode=true;
    }else{
      print("Turret Mode Disengaged!");
      isInTurretMode=false;
    }
    //socket.write("Turret Mode:$isInTurretMode");
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: Stack(
          fit: StackFit.expand,
          children: <Widget>[
            Container(
              color: Colors.amber,
              child: Mjpeg(
                stream: stream,
                isLive: true
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