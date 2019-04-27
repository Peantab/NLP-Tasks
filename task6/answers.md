# Answers

* Find all meanings of the *szkoda* **noun** and display all their synonyms. [Found on `http://plwordnet.pwr.wroc.pl/` website]
    * miejsce w polu lub ogrodzie, gdzie zwierzęta (np. drób, bydło) zniszczyły plony
    * mimowolna utrata czegoś, szkoda
        * strata 1
        * utrata 1
        * uszczerbek 1

* Find closure of **hypernymy** relation for the first meaning of the *wypadek drogowy* expression. Create diagram of the relations as a directed graph.

    Diagram generated with `http://plwordnet.pwr.wroc.pl/` website
    ![Diagram of the relations](wordnet-graph-wypadek.png)

* Find direct **hyponyms** of _wypadek<sub>1</sub>_ noun.

    Diagram created with [WordNetLoom-Viewer](http://ws.clarin-pl.eu/public/WordnetLoom-Viewer.zip)
    ![Diagram with hyponyms](wypadek.png)

* Find second-order **hyponyms** of the same noun.

    Only one new lexem - *kolizja drogowa* - was added.
    ![Diagram with second-order hyponyms](kolizja.png)

* Display as a directed graph (with labels for the edges) semantic relations between the following groups of lexemes:
    1. szkoda<sub>2</sub>, strata<sub>1</sub>, uszczerbek<sub>1</sub>, szkoda majątkowa<sub>1</sub>, uszczerbek na zdrowiu<sub>1</sub>, krzywda<sub>1</sub>, niesprawiedliwość<sub>1</sub>, nieszczęście<sub>2</sub>.

        Drawn in *LibreOffice Draw*, based on result of exploration in *WordNetLoom-Viewer*
        ![Directed graph of semantic relations in group 1](dag1.png)
    2. wypadek<sub>1</sub>, wypadek komunikacyjny<sub>1</sub>, kolizja<sub>2</sub>, zderzenie<sub>2</sub>, kolizja drogowa<sub>1</sub>, bezkolizyjny<sub>2</sub>, katastrofa budowlana<sub>1</sub>, wypadek drogowy<sub>1</sub>.

        ![Directed graph of semantic relations in group 2](dag2.png)

* Find the value of [Leacock-Chodorow semantic similarity measure](ftp://www-vhost.cs.toronto.edu/public_html/public_html/pub/gh/Budanitsky+Hirst-2001.pdf) between following pairs of lexemes:
    1. szkoda<sub>2</sub> - wypadek<sub>1</sub>,
    2. kolizja<sub>2</sub> - szkoda majątkowa<sub>1</sub>,
    3. nieszczęście<sub>2</sub> - katastrofa budowlana<sub>1</sub>.

    The Leacock-Chodorow semantic similarity measure is calculated with a formula: *lch(c<sub>1</sub>, c<sub>2</sub>) = -log (len(c<sub>1</sub>, c<sub>2</sub>) / (2 * D))*. *log* is a natural logarithm, *len* is amount of edges between nodes (at least in *nltk* implementation).
    
    First of all one has to find **D**. It is the overall depth of the taxonomy - in this case for nouns.

    The longest taxonomy for nouns is **35** items long: chirolog -> chiromanta -> wróżbiarz -> ezoteryk -> parapsycholog -> psycholog -> specjalista od nauk społecznych -> humanista -> uczony -> intelektualista -> mózg -> głowa -> człowiek określany jakoś ze względu na predyspozycje umysłowe -> człowiek o określonych predyspozycjach -> nazwa człowieka uwzględniająca jego cechy -> człowiek -> homo sapiens -> człowiek -> hominid -> małpa człekokształtna -> małpa wąskonosa -> małpa -> łożyskowiec -> ssak żyworodny -> ssak -> owodniowiec -> tetrapod -> kręgowiec -> czaszkowiec -> strunowiec -> zwierzę -> istota żywa -> organizm -> obiekt -> coś

    There are though 17623 different taxonomies for nouns, starting in for example: istota, coś, administracja, cecha, adres, miejsce, podmiot, wydarzenie, całość, Nowy Targ, sepecik, test-auto.

    Therefore, to have all nouns in one taxonomy, we add a special fake root, beeing a parent for all roots. **D** has then a value of **36**.

    1. szkoda<sub>2</sub> - wypadek<sub>1</sub>

        Path: szkoda<sub>2</sub> -> niepowodzenie<sub>1</sub> -> zdarzenie oceniane negatywnie<sub>1</sub> <- wypadek<sub>1</sub>
        
        len: 3
        
        **Leacock-Chodorow: 3.1781**

    2. kolizja<sub>2</sub> - szkoda majątkowa<sub>1</sub>

        Path: kolizja<sub>2</sub> -> wypadek<sub>1</sub> -> zdarzenie oceniane negatywnie<sub>1</sub> <- niepowodzenie<sub>1</sub> <- strata<sub>1</sub> <- szkoda majątkowa<sub>1</sub>

        len: 5

        **Leacock-Chodorow: 2.6672**
    
    3. nieszczęście<sub>2</sub> - katastrofa budowlana<sub>1</sub>

        Path: 
        * katastrofa budowlana<sub>1</sub> has exactly one derivation of length **3** and has no homonyms: wydarzenie<sub>1</sub> -> zdarzenie oceniane negatywnie<sub>1</sub> -> wypadek<sub>1</sub> -> katastrofa budowlana<sub>1</sub>; therefore it's path to fake root has a length of **4**.
        * nieszczęście<sub>2</sub> has to derivations, shorter of which is as follows: rzecz<sub>6</sub> -> rzecz oceniana negatywnie<sub>1</sub> -> zło<sub>1</sub> -> nieszczęście<sub>2</sub>. It's length is **3**, therefore to *fake root* it is **4**.

        len: *4+4=8*

        **Leacock-Chodorow: 2.1972**

Attached script performs calculations of **D** and carries out a proof that there is no single root for nouns.