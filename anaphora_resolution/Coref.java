import java.util.Scanner;
import java.util.Set;
import java.util.regex.Pattern;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Properties;

import edu.stanford.nlp.coref.CorefCoreAnnotations;
import edu.stanford.nlp.coref.CorefCoreAnnotations.CorefChainAnnotation;
import edu.stanford.nlp.coref.data.CorefChain;
import edu.stanford.nlp.coref.data.Dictionaries;
import edu.stanford.nlp.coref.data.CorefChain.CorefMention;
import edu.stanford.nlp.coref.data.Mention;
import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.ling.CoreAnnotations.TokensAnnotation;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.util.CoreMap;

public class CorefExample {
	static String[] pronouns = new String[] { "he", "she", "his", "him", "her", "they", "their" };
	
	public static void main(String[] args) throws Exception {
		// String filename =
		// "/Users/apple/Documents/workspace/coreNLP2/src/sample.txt";
		// String content = new Scanner(new
		// File(filename)).useDelimiter("\\Z").next();
		CorefExample ce = new CorefExample();
		String content = "Bill Cato, a Negro Saw Mill Hand, Attempted to Assault Mrs. Vickers. He Was Taken From the Doerun Guard House and Shot to Death. He Made Confession of Crime. News of a lynching which occurred at Doerun, Worth county, twenty-one miles from Albany to an early hour yesterday morning, reached the city today. It seems that an effort was made to keep the story of the lynching as quiet as possible, and the HERALD only learned of the affair this morning by chance. It appears that on last Monday night a negro saw mill hand named Bill Cato entered the home of a Mr. Vickers and attempted a criminal assault on Mrs. Vickers. His designs were frustrated by his intended victim’s screams and the interference of her husband. Cato made his escape. Next day he was captured, however, by some of the saw mill men of the neighborhood, who, strange to relate, let him off with a severe whipping and ordered him to leave the state. The negro departed, but unwisely remained in the neighborhood. When the people of Doerun heard of the crime they decided that Cato had not been sufficiently punished. They organized a search for him and finally succeeded in capturing him. He was placed in the Doerun guard house, and was not only identified by Mrs. Vickers as the right party, but, it is stated made a voluntary confession. At an early hour yesterday morning a mob of quiet but thoroughly determined men went to the guard house, forced the locks on the doors and took charge of Cato. He was carried outside and about seventy-five shots were fired into his body. His corpse was found after daylight within a few feet of the guard house door.";
		
		//Annotation doc = new Annotation(content);
		Properties props = new Properties();
		props.setProperty("annotators", "tokenize,ssplit,pos,lemma,ner,parse,mention,coref");
		StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
		String myDirectoryPath = "C:\\Users\\Doris\\Documents\\School\\Emory\\Research\\100txt";
		String outputFile;
		String inputFile;
		PrintWriter out;
		//getRepresentativeMentions("C:\\Users\\Doris\\Documents\\PC-ACE\\test\\corefex.txt", pipeline);
		System.out.println(ce.replaceMentions("C:\\Users\\Doris\\Documents\\PC-ACE\\test\\corefex.txt", pipeline));
		
		/*File dir = new File(myDirectoryPath);
		  File[] directoryListing = dir.listFiles();
		  if (directoryListing != null) {
		    for (File child : directoryListing) {
		      inputFile = child.getAbsolutePath();
		      System.out.println(inputFile);
		      outputFile = "C:\\Users\\Doris\\Documents\\School\\Emory\\Research\\100out\\" + child.getName().replaceFirst("[.][^.]+$", "") + "-out";
		      
		      out = new PrintWriter(outputFile + ".txt", "UTF-8");
		      
		      String resolved = ce.replaceMentions(inputFile, pipeline);
		      //resolved = resolved.replace("â $'' ", "—");
		      //resolved = resolved.replace("-LRB- ", "(");
		      //resolved = resolved.replace(" -RRB-", ")");
		      out.print(resolved);
		      
		      out.close();
		    }
		  } else {
		    // Handle the case where dir is not really a directory.
		    // Checking dir.isDirectory() above would not be sufficient
		    // to avoid race conditions with another process that deletes
		    // directories.
		  }*/
		
		  
		//ce.checkForUnresolvedPronouns(resolved);
	}
	
	public static void getRepresentativeMentions(String filename, StanfordCoreNLP pipeline) throws IOException {
		String content = readFile(filename);
		//System.out.println(content);
		Annotation doc = new Annotation(content);
		/*Properties props = new Properties();
		props.setProperty("annotators", "tokenize,ssplit,pos,lemma,ner,parse,mention,coref");*/
		//StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
		pipeline.annotate(doc);

		Map<Integer, CorefChain> corefs = doc.get(CorefChainAnnotation.class);
		for (Integer k : corefs.keySet()) {
			CorefChain cc = corefs.get(k);
			
			System.out.println("\n" + cc.toString());
			System.out.println(cc.getRepresentativeMention().mentionSpan + ", headID:" + cc.getRepresentativeMention().headIndex + ", sent:" + cc.getRepresentativeMention().sentNum);
		}
		
	}
	
	/**
	 * Attempts to resolve coreferences to animate objects in the given file.
	 * @param filename - text file to read and edit content of
	 * @return String with resolved coreferences
	 * @throws IOException 
	 */
	public String replaceMentions(String filename, StanfordCoreNLP pipeline) throws IOException {
		String content = readFile(filename);
		//System.out.println(content);
		Annotation doc = new Annotation(content);
		/*Properties props = new Properties();
		props.setProperty("annotators", "tokenize,ssplit,pos,lemma,ner,parse,mention,coref");*/
		//StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
		pipeline.annotate(doc);

		Map<Integer, CorefChain> corefs = doc.get(CorefChainAnnotation.class);
		List<CoreMap> sentences = doc.get(CoreAnnotations.SentencesAnnotation.class);

		List<String> resolved = new ArrayList<String>();

		for (CoreMap sentence : sentences) {
			//System.out.println(sentence);
			List<CoreLabel> tokens = sentence.get(CoreAnnotations.TokensAnnotation.class);

			for (CoreLabel token : tokens) {

				Integer corefClustId = token.get(CorefCoreAnnotations.CorefClusterIdAnnotation.class);
				//System.out.println(token.word() + " --> corefClusterID = " + corefClustId);

				CorefChain chain = corefs.get(corefClustId);
				
				//ignore tokens with no chain
				if (chain == null) {
					// if (!reprMent.mentionSpan.contains(token.word()))
					resolved.add(token.word());
					continue;
				}

				// pre-processing of chain
				boolean male = false;
				boolean female = false;
				boolean animate = false;
				for (CorefMention m : chain.getMentionsInTextualOrder()) {
					if (m.gender == Dictionaries.Gender.FEMALE) {
						female = true;
					} else if (m.gender == Dictionaries.Gender.MALE) {
						male = true;
					}
					
					if (m.animacy == Dictionaries.Animacy.ANIMATE) {
						animate = true;
					}
				}
				
				//ignore tokens that are not animate or come from a chain with conflicting gender
				if (female && male || !animate) {
					//System.out.println(chain.toString() + " ignored for " + token.word());
					resolved.add(token.word());
					continue;
				} else {
					//replace token with representative mention
					CorefMention reprMent = chain.getRepresentativeMention();
					if (token.index() == reprMent.headIndex && token.sentIndex()+1 == reprMent.sentNum) {
						//is head of representative mention, no need to replace
						resolved.add(token.word());
					} else {
						String j = reprMent.mentionSpan;
						String[] reprWords = j.split(" ");
						
						if (token.tag().equals("PRP$"))	{
							//append "'s" for possessive pronouns
							for (int i = 0; i < reprWords.length-1; i++) {
								resolved.add(reprWords[i]);
							}
							resolved.add(reprWords[reprWords.length-1] + "'s");
						} else {
							for (int i = 0; i < reprWords.length; i++) {
								resolved.add(reprWords[i]);
							}
						}
					}
				}

			}

		}
		
		//remove duplicate words
		for (int i = 1; i < resolved.size(); i++) {
			//System.out.println(resolved.get(i));
			if (resolved.get(i-1).equals(resolved.get(i))) {
				//System.out.println(resolved.get(i) + " removed");
				resolved.remove(i);
				i--;
			} else if ( (resolved.get(i-1).equalsIgnoreCase("the") || resolved.get(i-1).equalsIgnoreCase("a")) 
					&& (resolved.get(i).equalsIgnoreCase("the") || resolved.get(i).equalsIgnoreCase("a")) ) {
				//System.out.println(resolved.get(i) + " removed");
				resolved.remove(i);
				i--;
			}
		}

		String resolvedStr = "";
		if (resolved.size() > 0) resolvedStr += resolved.get(0) + " ";
		for (int i = 1; i < resolved.size(); i++) {
			//fix capitalization following end punctuation
			String str = resolved.get(i);
			String prev = resolved.get(i-1);
			String endPunct = ".!?'";
			if (endPunct.contains(prev)) {
				str = str.substring(0, 1).toUpperCase() + str.substring(1);
			}
			
			//add word to final string
			resolvedStr += str + " ";
		}

		resolvedStr = cleanOutput(resolvedStr);

		return resolvedStr;
	}
	
	/**
	 * Removes extraneous spaces in input.
	 * @param resolvedStr - String to clean
	 * @return cleaned string
	 */
	public String cleanOutput(String resolvedStr) {
		// fix spacing around punctuation
		String punct = ".,:;!?'";
		for (int i = 1; i < resolvedStr.length(); i++) {
			if (punct.contains("" + resolvedStr.charAt(i)) && resolvedStr.charAt(i - 1) == ' ') {
				resolvedStr = resolvedStr.substring(0, i - 1) + resolvedStr.substring(i, resolvedStr.length());
				i--;
			}
		}

		resolvedStr.trim();
		return resolvedStr;
	}
	
	/**
	 * Checks if any words in the input are a pronoun.
	 * Pronouns = "he", "she", "his", "him", "her", "they", "their"
	 * @param input - input String to check through
	 */
	public void checkForUnresolvedPronouns(String input) {
		Annotation doc = new Annotation(input);
		Properties props = new Properties();
		props.setProperty("annotators", "tokenize,ssplit,pos,lemma,ner,parse,mention");
		StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
		pipeline.annotate(doc);

		List<CoreMap> sentences = doc.get(CoreAnnotations.SentencesAnnotation.class);

		for (CoreMap sentence : sentences) {
			//System.out.println(sentence);
			List<CoreLabel> tokens = sentence.get(CoreAnnotations.TokensAnnotation.class);

			for (CoreLabel token : tokens) {
				for (String s : pronouns) {
					if (token.word().equalsIgnoreCase(s)) {
						System.out.println("In sentence: " + sentence);
						System.out.println(token.word() + " at index " + token.index());
					}
				}
			}
		}
	}
	
	//http://stackoverflow.com/questions/4716503/reading-a-plain-text-file-in-java
	/**
	 * Reads a text file into a String.
	 * @param pathname - path of source file to turn into a String
	 * @return file content as a String
	 * @throws IOException
	 */
	private static String readFile(String pathname) throws IOException {

		try(BufferedReader br = new BufferedReader(new FileReader(pathname))) {
		    StringBuilder sb = new StringBuilder();
		    String line = br.readLine();

		    while (line != null) {
		        sb.append(line);
		        sb.append(System.lineSeparator());
		        line = br.readLine(); 
		    }
		    String everything = sb.toString();
		    
		    return everything;
		}
	}
}
