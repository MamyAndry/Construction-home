def xstr(s):
    return '' if s is None else str(s)

def get_html_for_pdf(devis, details):
    res = """
    <style>
        td,th {border:solid 1px black; padding-top: 5px; padding-bottom: 5px;}
        td{
            border-bottom : 0; border-top: 0
        }
        .last{
            border: solid 1px black;
        }
    </style>
    <center><h2>DEVIS</h2></center>
    <div>
        <h5> <i>Client</i> : """ + devis.client.numero + """ </h5>        
        <h5> <i>Date devis</i>  : """ + str(devis.date_devis) + """</h5>
        <h5> <i>Date debut construction : </i>""" + str(devis.date_debut_construction) + """ </h5><br>
        <h5> <i>Type Maison</i> : """ + devis.type.libelle + """ </h5>        
        <h5> <i>Finition</i>  : """ + devis.finition.libelle + """</h5>  
        <h5> <i>Pourcentage</i>  : """ + str(devis.pourcentage) + """ % </h5>        
        <h5> <i>Prix total</i> :""" + str(f"{devis.prix_total:,.2f}") + """ </h5>
    </div>
    <center><table>
    <tr>
        <th>NUMERO</th>
        <th>DESIGNATION</th>
        <th>UNITE</th>
        <th>QUANTITE</th>
        <th>PRIX UNITAIRE</th>
        <th>TOTAL</th>
    </tr>
    """
    total = 0
    for elt in details:
        qte = str(f"{elt.quantite:,.2f}")
        pu = str(f"{elt.prix_unitaire:,.2f}")
        prix_total = str(f"{(elt.quantite * elt.prix_unitaire):,.2f}")
        total += elt.quantite * elt.prix_unitaire
        res += """
        <tr>
            <td>
                """ + xstr(elt.travaux.code) + """
            </td>
            <td>
                """ + xstr(elt.travaux.libelle) +"""
            </td>                   
            <td>
                """ + xstr(elt.travaux.unite.libelle) + """
            </td>                    
            <td>
                """ + qte + """
            </td> 
            <td>
                """ + pu + """
            </td>                    
            <td>
                """ + prix_total + """
            </td>
        </tr>"""
    res += """
        <tr>
            <td class="last"></td><td class="last"></td><td class="last"></td><td class="last"></td><td class="last"><strong>TOTAL</strong></td><td class="last"><strong>""" + str(f"{total:,.2f}") + """</strong></td>
        </tr></table></center>"""
    return res
    res += """"""
