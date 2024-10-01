package application;

import java.io.IOException;

import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.stage.Stage;

public class IrisUnmatchedController {

	@FXML
	private Button btnTryAgain;
	@FXML
	private Button btnExitTransaction;

	public void TryAgain(ActionEvent event){
		try {
			FXMLLoader loader=new FXMLLoader(getClass().getResource("Bank_Customer_Login_2.fxml"));
			Parent root = (Parent)loader.load();
			Stage window = (Stage)((Node)event.getSource()).getScene().getWindow();	// It  is used to get Window information
			Bank_Customer_Login_2Controller bank_Customer_Login_2Controller= loader.getController();
			bank_Customer_Login_2Controller.setDisebleButton(false);
			Scene scene = new Scene(root);
	        window.setScene(scene);
	        window.setFullScreen(true);
			window.show();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} 
	}

	public void ExitTransaction(ActionEvent event){
		try {
			Parent root = FXMLLoader.load(getClass().getResource("Bank_ClientLogin_1st_page.fxml"));
			Stage window = (Stage)((Node)event.getSource()).getScene().getWindow();	// It  is used to get Window information
	        Scene scene = new Scene(root);
	        window.setScene(scene);
	        window.setFullScreen(true);
			window.show();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} 
	}
}
