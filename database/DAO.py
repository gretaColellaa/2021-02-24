from database.DB_connect import DBConnect


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getMatches():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct m.MatchID 
                    from premierleague.matches m """

        cursor.execute(query)

        for row in cursor:
            result.append(row["MatchID"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getNodi(m):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct a.PlayerID 
                    from premierleague.actions a 
                    where a.MatchID = %s
                    """

        cursor.execute(query, (m,))

        for row in cursor:
            result.append(row["PlayerID"])

        cursor.close()
        conn.close()
        return result




    @staticmethod
    def getEfficienza(p,m):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select  a.TeamID , a.TotalSuccessfulPassesAll , a.Assists , a.TimePlayed
                    from premierleague.actions a
                    where a.PlayerID = %s
                    and a.MatchID = %s
                    """

        cursor.execute(query, (p,m,))

        for row in cursor:
            try: e = (int(row["TotalSuccessfulPassesAll"]) + int(row["Assists"]))/int(row["TimePlayed"])
            except: e = None


            result.append((row["TeamID"], e))

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def getTeams(m):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT m.TeamHomeID , m.TeamAwayID 
                    FROM premierleague.matches m 
                    where m.MatchID = %s
                            """

        cursor.execute(query, (m,))

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()
        return result

