import java.util.ArrayList;
import java.util.Scanner;

class Simplex{
    double[] co_ob;//coefficient of objective function
    ArrayList<double[]> matrix;//coefficient of inequalities function
    double[] sol;//vector of solution
    int approx;//Approximation accuracy
    double[][] table;//table with solution and coefficient
    public void show_table_st() {
        String string;
        System.out.print("Maximize z =");
        for (int i = 0; i < co_ob.length; i++) {
            string = Integer.toString(i+1);
            System.out.print(" + " + co_ob[i] + " * " + "x" + string );
            if (i == co_ob.length - 1) {
                System.out.print("\n");
            }
        }
        System.out.println("subject to the constraints:");
        for (int i=0;i< matrix.size();i++){
            for (int j=0;j<matrix.get(i).length;j++){
                string = Integer.toString(j+1);
                if (j!=0) {
                    System.out.print( " + " + matrix.get(i)[j] + " * " + "x" + string);
                }else{
                    System.out.print(+ matrix.get(i)[j] + " * " + "x" + string);

                }
            }
            System.out.println(" <= " + sol[i+1]);
        }

    }
    public void get_data(){
        Scanner sc = new Scanner(System.in);
        String[] str = sc.nextLine().split(" ");
        int co_len = str.length;
        co_ob = new double[co_len];
        for (int i = 0; i < co_len; i++) {
            co_ob[i] = Double.parseDouble(str[i]);
        }
        int len_col = co_ob.length;
        str = sc.nextLine().split(" ");
        double[] mat_row = new double[len_col];
        matrix = new ArrayList<>();
        while (str.length == len_col){
            mat_row = new double[len_col];
            for (int i=0;i<len_col;i++){
                mat_row[i]=0;
                mat_row[i] = Double.parseDouble(str[i]);
            }
            matrix.add(mat_row);
            str = sc.nextLine().split(" ");
        }

        if (str.length == matrix.size()){
            sol = new double[str.length];
            for (int i=0; i< str.length;i++){
                sol[i] = Double.parseDouble(str[i]);
            }
            str = sc.nextLine().split(" ");
            approx = countDecimalPlaces(str[0]);
        }else{
            sol = new double[mat_row.length];
            System.arraycopy(mat_row, 0, sol, 0, len_col);
            matrix.remove(matrix.size()-1);
            approx = countDecimalPlaces(str[0]);
        }
    }
    public int countDecimalPlaces(String number) {
        String[] parts = number.split("\\.");
        if (parts.length == 2 && !parts[1].isEmpty()) {
            return parts[1].length();
        }
        return 0;
    }
}
public class Main {
    public static void main(String[] args) {
        
    }
}
