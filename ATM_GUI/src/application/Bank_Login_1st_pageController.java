//First Admin login page

package application;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.stage.Stage;

public class Bank_Login_1st_pageController
 {
    @FXML
    private TextField txtUser;
    @FXML
    private TextField txtPassword;
    @FXML
    private Label labelLoginFailed; 
    public void Login(ActionEvent event) {
        if((txtUser.getText().equals("atm"))&&(txtPassword.getText().equals("1"))){
            labelLoginFailed.setText("Login Successfull!!");
            try {
                Parent root = FXMLLoader.load(getClass().getResource("Bank_ClientLogin_1st_page.fxml")); 
                Stage window = (Stage)((Node)event.getSource()).getScene().getWindow();	// It  is used to get Window information
                Scene scene = new Scene(root);
                window.setScene(scene);
                window.setFullScreen(true);
                window.show();
            } catch (Exception e) {
                //TODO: handle exception
            }
        }else{
            labelLoginFailed.setText("Username or Password is wrong!!");
        }
    }
    public void Reset(ActionEvent event) {
        txtUser.setText("");
        txtPassword.setText("");
    }
    public void exit(ActionEvent event) {
        System.exit(1);
    }
}
