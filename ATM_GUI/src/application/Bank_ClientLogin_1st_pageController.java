//Fist Customer Bank selection page
package application;

import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.fxml.Initializable;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.stage.Stage;

import java.net.URL;
import java.util.ResourceBundle;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.event.ActionEvent;


public class Bank_ClientLogin_1st_pageController implements Initializable{
	@FXML
	private Button btnGenericBank;
	@FXML
	private ComboBox<String> cboxOtherBank;
	ObservableList<String> list = FXCollections.observableArrayList("ICICI Bank","Punjab National Bank(PNB)","State Bank of India(SBI)");
	@FXML
	private Button btnProceed;

	@FXML
	public void ContinueAsGenericBank(ActionEvent event) {
		try {
			FXMLLoader loader=new FXMLLoader(getClass().getResource("Bank_Customer_Login_2.fxml"));
			Parent root = (Parent)loader.load();
			Stage window = (Stage)((Node)event.getSource()).getScene().getWindow();	// It  is used to get Window information
			Bank_Customer_Login_2Controller bank_Customer_Login_2Controller= loader.getController();
			bank_Customer_Login_2Controller.setDisebleButton(true);
			Scene scene = new Scene(root);
	        window.setScene(scene);
	        window.setFullScreen(true);
			window.show();
        } catch (Exception e) {
            //TODO: handle exception
		}
	}

	@FXML
	public void Select() {
		btnProceed.setDisable(false);
	}

	@FXML
	public void Proceed() {
		
	}

	@Override
	public void initialize(URL location, ResourceBundle resources) {
		// TODO Auto-generated method stub
		cboxOtherBank.setItems(list);
	}
}
