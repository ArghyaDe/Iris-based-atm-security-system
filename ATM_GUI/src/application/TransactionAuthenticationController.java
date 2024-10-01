package application;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.PrintStream;
import java.util.ArrayList;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Node;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.ComboBox;
import javafx.scene.control.TextField;
import javafx.stage.Stage;

public class TransactionAuthenticationController {
	private String UName,UserId,email,accountno,scrt;
	private int ammount=0,itemNo=-1;
	private ArrayList<Integer> accountserial=new ArrayList<Integer>();
	@FXML
	private ComboBox<String> cboxAccountPicker;
	ObservableList<String> list = FXCollections.observableArrayList();

	@FXML
	private TextField txtAmount;

	@FXML
	private TextField txtSecretKey;

	@FXML
	private Button btnNext;

	@FXML
	private Button btnReset;

	@FXML
	private Button btnexit;
	
	@FXML
	public void SelectAccuntNo(ActionEvent event) {
		try {
			int a=list.indexOf(cboxAccountPicker.getValue());
			itemNo=accountserial.get(a);
			accountno=cboxAccountPicker.getValue();
			System.out.print(itemNo);
		}catch(Exception e) {
			itemNo=-1;
		}
	}

	@FXML
	public void Next(ActionEvent event) {
		boolean tran=false;
		try {
			ammount=Integer.parseInt(txtAmount.getText());
			scrt=txtSecretKey.getText();
		}catch(Exception e) {
			itemNo=-1;
			scrt="";
		}
		if(ammount!=-1&&scrt.isEmpty()==false&&itemNo!=-1) {
			try {
				final String command[]={"python","Transacrion.py"};
		        final ProcessBuilder pd = new ProcessBuilder(command);
				final Process p = pd.start();
				final OutputStream os = p.getOutputStream();
		        final PrintStream ps= new PrintStream(os);
		        ps.println(UserId);
		        ps.flush();
		        ps.println(scrt);
		        ps.flush();
		        ps.println(itemNo);
		        ps.flush();
		        ps.println(ammount);
		        ps.flush();
		        ps.println("AtmSecurity4444");
		        ps.flush();
		        final BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));
				String line;
				while((line=br.readLine()).isEmpty()==false) {
					if(line.equals("success")) {
						tran=true;
					}
				}
			}catch(Exception e){
				System.out.print(e);
			}
			try {
				if(tran==true) {
					Parent root = FXMLLoader.load(getClass().getResource("TransactionSuccessful.fxml")); 
			        Stage window = (Stage)((Node)event.getSource()).getScene().getWindow();	// It  is used to get Window information
			        Scene scene = new Scene(root);
			        window.setScene(scene);
			        window.setFullScreen(true);
					window.show();
					Thread.sleep(10000);
					root=FXMLLoader.load(getClass().getResource("Bank_ClientLogin_1st_page.fxml"));
					scene = new Scene(root);
					window.setScene(scene);
			        window.setFullScreen(true);
					window.show();
				}else {
					Parent root = FXMLLoader.load(getClass().getResource("TransactionFailed.fxml")); 
			        Stage window = (Stage)((Node)event.getSource()).getScene().getWindow();	// It  is used to get Window information
			        Scene scene = new Scene(root);
			        window.setScene(scene);
			        window.setFullScreen(true);
					window.show();
					Thread.sleep(10000);
					root=FXMLLoader.load(getClass().getResource("Bank_ClientLogin_1st_page.fxml"));
					scene = new Scene(root);
					window.setScene(scene);
			        window.setFullScreen(true);
					window.show();
				}
			}catch(Exception e) {
				System.out.print(e);
			}
		}
	}

	@FXML
	public void Reset(ActionEvent event) {
		txtAmount.setText("");
		txtSecretKey.setText("");
	}

	@FXML
	public void Exit(ActionEvent event){
		try {
            Parent root = FXMLLoader.load(getClass().getResource("Bank_ClientLogin_1st_page.fxml")); 
            Stage window = (Stage)((Node)event.getSource()).getScene().getWindow();	// It  is used to get Window information
            Scene scene = new Scene(root);
            window.setScene(scene);
            window.setFullScreen(true);
			window.show();
        } catch (Exception e) {
            //TODO: handle exception
        	System.out.print(e);
        }
	}
	
	public void setAll(String UName,String UserId,String email,String Bank[],String AccountNo[]){
		this.UName=new String(UName);
		this.email=new String(email);
		this.UserId=new String(UserId);
		for(int i=0;i<Bank.length;i++) {
			if(Bank[i].equals("GENERIC")) {
				this.list.add(new String(AccountNo[i].substring(0, 2)+"xx xxxx xx"+AccountNo[i].substring(10,12)));
				this.accountserial.add(i);
			}
		}
		cboxAccountPicker.getItems().addAll(list);
	}

}
