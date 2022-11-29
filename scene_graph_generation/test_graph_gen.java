import edu.stanford.nlp.scenegraph.RuleBasedParser;
import edu.stanford.nlp.scenegraph.SceneGraph;

public class test_graph_gen {

    public static void main(String[] args)
    {
        String sentence = "A brown fox chases a white rabbit.";

        RuleBasedParser parser = new RuleBasedParser();
        SceneGraph sg = parser.parse(sentence);

        //printing the scene graph in a readable format
        String readable_string = sg.toReadableString();
        System.out.println(readable_string); 

        //printing the scene graph in JSON form
        System.out.println(readable_string.toJSON()); 
    }
}
