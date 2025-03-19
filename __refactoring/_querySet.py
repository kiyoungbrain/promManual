import re


# 부담금 querySet

부담금_sample = {
    "main_web": {
        "queries1": """
        """,
        "queries2": """
        """,
        "queries4": """
        """
    },
    "report_web": {
        "query1": """
        """,
        "query2": """
        """
    },
    "shop_detail": {
        "분담금": """
        """,
        "총합계": """
        """,
        "과금1차": """
        """,
        "과금2차": """
        """
    }
}


_03_배민_부담금_VIP = {
    "main_web": {
        "queries1": """
            -- _03_배민_부담금_[VIP]
            (
                SELECT
                    brand,
                    '배민' AS 업체,
                    프로모션_구분 AS 프로모션,
                    쿠폰사용금액 AS 금액,
                    YM,
                    CONCAT(DATE_FORMAT(MIN(사용일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(사용일자), '%m-%d')) AS 기간,
                    0 AS 쿠폰건수,
                    -1 * (
                        CASE
                            WHEN 쿠폰사용금액 IN (3500, 4500) THEN 500 * COUNT(CASE WHEN 정산금액 != 0 THEN 1 END)
                            WHEN 쿠폰사용금액 IN (4000, 5000) THEN 1000 * COUNT(CASE WHEN 정산금액 != 0 THEN 1 END)
                            ELSE 0
                        END
                    ) AS 합계
                FROM
                    prom_baemin
                WHERE
                    YM IN ('202403', '202406', '202407', '202408', '202410', '202412', '202501', '202502') 
                    AND 프로모션_구분 LIKE '%VIP%' 
                    AND 쿠폰사용금액 IN (3500, 4000, 4500, 5000)
                GROUP BY
                    brand, 업체, 프로모션, 금액, YM
            )
            UNION ALL\n
        """,
        "queries2": """
            -- _03_배민_부담금_[VIP] (프로모션, 배민 지원금 (두찜: 3500-500, 4500-1000 / 떡참: 4500-500, 5000-1000 / 숯불: 4000-1000, 3500-500))
            WHEN YM IN ('202403', '202406', '202407', '202408') AND 프로모션_구분 LIKE '%VIP%' AND (쿠폰사용금액 = 3500 OR 쿠폰사용금액 = 4500) THEN ((쿠폰사용금액 - 500) * 0.6) * (COUNT(CASE WHEN 정산금액 != 0 THEN 1 END))
            WHEN YM IN ('202403', '202406', '202407', '202408') AND 프로모션_구분 LIKE '%VIP%' AND (쿠폰사용금액 = 4000 OR 쿠폰사용금액 = 5000) THEN ((쿠폰사용금액 - 1000) * 0.6) * (COUNT(CASE WHEN 정산금액 != 0 THEN 1 END))
            WHEN YM IN ('202410', '202412', '202501', '202502') AND 프로모션_구분 LIKE '%VIP%' AND (쿠폰사용금액 = 3500 OR 쿠폰사용금액 = 4500) THEN ((쿠폰사용금액 - 500) * 0.5) * (COUNT(CASE WHEN 정산금액 != 0 THEN 1 END))
            WHEN YM IN ('202410', '202412', '202501', '202502') AND 프로모션_구분 LIKE '%VIP%' AND (쿠폰사용금액 = 4000 OR 쿠폰사용금액 = 5000) THEN ((쿠폰사용금액 - 1000) * 0.5) * (COUNT(CASE WHEN 정산금액 != 0 THEN 1 END))
        """,
        "queries4": """
            -- _03_배민_부담금_[VIP] (프로모션, 배민 지원금 (두찜: 3500-500, 4500-1000 / 떡참: 4500-500, 5000-1000 / 숯불: 4000-1000, 3500-500))
            WHEN YM IN ('202403', '202406', '202407', '202408') AND 프로모션_구분 LIKE '%VIP%' AND (쿠폰사용금액 = 3500 OR 쿠폰사용금액 = 4500) THEN ((쿠폰사용금액 - 500) * 0.6) * (COUNT(CASE WHEN 정산금액 != 0 THEN 1 END))
            WHEN YM IN ('202403', '202406', '202407', '202408') AND 프로모션_구분 LIKE '%VIP%' AND (쿠폰사용금액 = 4000 OR 쿠폰사용금액 = 5000) THEN ((쿠폰사용금액 - 1000) * 0.6) * (COUNT(CASE WHEN 정산금액 != 0 THEN 1 END))
            WHEN YM IN ('202410', '202412', '202501', '202502') AND 프로모션_구분 LIKE '%VIP%' AND (쿠폰사용금액 = 3500 OR 쿠폰사용금액 = 4500) THEN ((쿠폰사용금액 - 500) * 0.5) * (COUNT(CASE WHEN 정산금액 != 0 THEN 1 END))
            WHEN YM IN ('202410', '202412', '202501', '202502') AND 프로모션_구분 LIKE '%VIP%' AND (쿠폰사용금액 = 4000 OR 쿠폰사용금액 = 5000) THEN ((쿠폰사용금액 - 1000) * 0.5) * (COUNT(CASE WHEN 정산금액 != 0 THEN 1 END))
        """
    },
    "report_web": {
        "query1": """
        	-- _03_배민_부담금_[VIP]
            SELECT
                YM,
                brand,
                프로모션_구분,
                CONCAT(DATE_FORMAT(MIN(사용일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(사용일자), '%m-%d')) AS 기간,
                '-' AS 쿠폰건수,
                SUM(CASE 
                        WHEN ((YM >= '202401' AND YM <= '202408') OR (YM = '202409' AND MONTH(사용일자) = 8)) AND 쿠폰사용금액 IN (3500, 4500) THEN -1 * 500 * 0.4 
                        WHEN ((YM >= '202401' AND YM <= '202408') OR (YM = '202409' AND MONTH(사용일자) = 8)) AND 쿠폰사용금액 IN (4000, 5000) THEN -1 * 1000 * 0.4 
                        WHEN YM >= '202409' AND 쿠폰사용금액 IN (3500, 4500) THEN -1 * 500 * 0.5
                        WHEN YM >= '202409' AND 쿠폰사용금액 IN (4000, 5000) THEN -1 * 1000 * 0.5
                        ELSE 0
                    END) AS 본사분담금,
                SUM(CASE 
                        WHEN ((YM >= '202401' AND YM <= '202408') OR (YM = '202409' AND MONTH(사용일자) = 8)) AND 쿠폰사용금액 IN (3500, 4500) THEN -1 * 500 * 0.6 
                        WHEN ((YM >= '202401' AND YM <= '202408') OR (YM = '202409' AND MONTH(사용일자) = 8)) AND 쿠폰사용금액 IN (4000, 5000) THEN -1 * 1000 * 0.6 
                        WHEN YM >= '202409' AND 쿠폰사용금액 IN (3500, 4500) THEN -1 * 500 * 0.5
                        WHEN YM >= '202409' AND 쿠폰사용금액 IN (4000, 5000) THEN -1 * 1000 * 0.5
                        ELSE 0
                    END) AS 가맹점분담금,
                '' AS 광고분담금,
                SUM(CASE 
                        WHEN 쿠폰사용금액 IN (3500, 4500) THEN -1 * 500
                        WHEN 쿠폰사용금액 IN (4000, 5000) THEN -1 * 1000
                        ELSE 0
                    END) AS 합계
            FROM prom_baemin
            WHERE YM IN ('202403', '202406', '202407', '202408', '202410', '202412', '202501', '202502') AND 프로모션_구분 LIKE '%VIP%' AND 쿠폰사용금액 IN (3500, 4000, 4500, 5000)
            GROUP BY YM, brand, 프로모션_구분
            UNION ALL\n
        """,
        "query2": """
            -- _03_배민_부담금_[VIP]
            SELECT
                YM,
                brand,
                프로모션_구분 AS 내용,
                CONCAT(DATE_FORMAT(MIN(사용일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(사용일자), '%m-%d')) AS 날짜,
                쿠폰사용금액 AS 금액,
                '-' AS 쿠폰건수_전체,
                SUM(CASE 
                        WHEN 쿠폰사용금액 IN (3500, 4500) THEN -1 * 500
                        WHEN 쿠폰사용금액 IN (4000, 5000) THEN -1 * 1000
                        ELSE 0
                    END) AS 납부금액_전체,
                CASE 
                    WHEN ((YM >= '202401' AND YM <= '202408') OR (YM = '202409' AND MONTH(사용일자) = 8)) AND 쿠폰사용금액 IN (3500, 4500) THEN (쿠폰사용금액 - 500) * 0.4 
                    WHEN ((YM >= '202401' AND YM <= '202408') OR (YM = '202409' AND MONTH(사용일자) = 8)) AND 쿠폰사용금액 IN (4000, 5000) THEN (쿠폰사용금액 - 1000) * 0.4 
                    WHEN YM >= '202409' AND 쿠폰사용금액 IN (3500, 4500) THEN -1 * 500 * 0.5
                    WHEN YM >= '202409' AND 쿠폰사용금액 IN (4000, 5000) THEN -1 * 1000 * 0.5
                    ELSE 0
                END AS 분담액_본사,
                SUM(CASE 
                        WHEN ((YM >= '202401' AND YM <= '202408') OR (YM = '202409' AND MONTH(사용일자) = 8)) AND 쿠폰사용금액 IN (3500, 4500) THEN -1 * 500 * 0.4 
                        WHEN ((YM >= '202401' AND YM <= '202408') OR (YM = '202409' AND MONTH(사용일자) = 8)) AND 쿠폰사용금액 IN (4000, 5000) THEN -1 * 1000 * 0.4 
                        WHEN YM >= '202409' AND 쿠폰사용금액 IN (3500, 4500) THEN -1 * 500 * 0.5
                        WHEN YM >= '202409' AND 쿠폰사용금액 IN (4000, 5000) THEN -1 * 1000 * 0.5
                        ELSE 0
                    END) AS 본사_분담액,
                CASE 
                    WHEN ((YM >= '202401' AND YM <= '202408') OR (YM = '202409' AND MONTH(사용일자) = 8)) AND 쿠폰사용금액 IN (3500, 4500) THEN (쿠폰사용금액 - 500) * 0.6
                    WHEN ((YM >= '202401' AND YM <= '202408') OR (YM = '202409' AND MONTH(사용일자) = 8)) AND 쿠폰사용금액 IN (4000, 5000) THEN (쿠폰사용금액 - 1000) * 0.6
                    WHEN YM >= '202409' AND 쿠폰사용금액 IN (3500, 4500) THEN -1 * 500 * 0.5
                    WHEN YM >= '202409' AND 쿠폰사용금액 IN (4000, 5000) THEN -1 * 1000 * 0.5
                    ELSE 0
                END AS 분담액_가맹,
                SUM(CASE 
                        WHEN ((YM >= '202401' AND YM <= '202408') OR (YM = '202409' AND MONTH(사용일자) = 8)) AND 쿠폰사용금액 IN (3500, 4500) THEN -1 * 500 * 0.6 
                        WHEN ((YM >= '202401' AND YM <= '202408') OR (YM = '202409' AND MONTH(사용일자) = 8)) AND 쿠폰사용금액 IN (4000, 5000) THEN -1 * 1000 * 0.6 
                        WHEN YM >= '202409' AND 쿠폰사용금액 IN (3500, 4500) THEN -1 * 500 * 0.5
                        WHEN YM >= '202409' AND 쿠폰사용금액 IN (4000, 5000) THEN -1 * 1000 * 0.5
                        ELSE 0
                    END) AS 합계_가맹,
                '' AS 분담액,
                '' AS 지원금액
            FROM prom_baemin
            WHERE YM IN ('202403', '202406', '202407', '202408', '202410', '202412', '202501', '202502') AND 프로모션_구분 LIKE '%VIP%' AND 쿠폰사용금액 IN (3500, 4000, 4500, 5000)
            GROUP BY YM, brand, 내용, 금액, 사용일자
            UNION ALL\n
        """
    },
    "shop_detail": {
        "분담금": """
            -- _03_배민_부담금_[VIP]
            WHEN YM IN ('202403', '202406', '202407', '202408') AND 프로모션_구분 LIKE '%VIP%' AND 정산금액 IN (3500, 4500) THEN ROUND(((정산금액 - 500) * 0.6), 1)
            WHEN YM IN ('202403', '202406', '202407', '202408') AND 프로모션_구분 LIKE '%VIP%' AND 정산금액 IN (4000, 5000) THEN ROUND(((정산금액 - 1000) * 0.6), 1)
            WHEN YM IN ('202410', '202412', '202501', '202502') AND 프로모션_구분 LIKE '%VIP%' AND 정산금액 IN (3500, 4500) THEN ROUND(((정산금액 - 500) * 0.5), 1)
            WHEN YM IN ('202410', '202412', '202501', '202502') AND 프로모션_구분 LIKE '%VIP%' AND 정산금액 IN (4000, 5000) THEN ROUND(((정산금액 - 1000) * 0.5), 1)
        """,
        "총합계": """
            -- _03_배민_부담금_[VIP]
            WHEN YM IN ('202403', '202406', '202407', '202408') AND 프로모션_구분 LIKE '%VIP%' AND 정산금액 IN (3500, 4500) THEN ((정산금액 - 500) * 0.6) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END)
            WHEN YM IN ('202403', '202406', '202407', '202408') AND 프로모션_구분 LIKE '%VIP%' AND 정산금액 IN (4000, 5000) THEN ((정산금액 - 1000) * 0.6) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END)
            WHEN YM IN ('202410', '202412', '202501', '202502') AND 프로모션_구분 LIKE '%VIP%' AND 정산금액 IN (3500, 4500) THEN ((정산금액 - 500) * 0.5) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END)
            WHEN YM IN ('202410', '202412', '202501', '202502') AND 프로모션_구분 LIKE '%VIP%' AND 정산금액 IN (4000, 5000) THEN ((정산금액 - 1000) * 0.5) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END)
        """,
        "과금1차": """
            -- _03_배민_부담금_[VIP]
            WHEN YM IN ('202403', '202406', '202407', '202408') AND 프로모션_구분 LIKE '%VIP%' AND 정산금액 IN (3500, 4500) THEN (((정산금액 - 500) * 0.6) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END)) / 2
            WHEN YM IN ('202403', '202406', '202407', '202408') AND 프로모션_구분 LIKE '%VIP%' AND 정산금액 IN (4000, 5000) THEN (((정산금액 - 1000) * 0.6) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END)) / 2
            WHEN YM IN ('202410', '202412', '202501', '202502') AND 프로모션_구분 LIKE '%VIP%' AND 정산금액 IN (3500, 4500) THEN (((정산금액 - 500) * 0.5) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END)) / 2
            WHEN YM IN ('202410', '202412', '202501', '202502') AND 프로모션_구분 LIKE '%VIP%' AND 정산금액 IN (4000, 5000) THEN (((정산금액 - 1000) * 0.5) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END)) / 2
        """,
        "과금2차": """
            -- _03_배민_부담금_[VIP]
            WHEN YM IN ('202403', '202406', '202407', '202408') AND 프로모션_구분 LIKE '%VIP%' AND 정산금액 IN (3500, 4500) THEN (((정산금액 - 500) * 0.6) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END)) / 2
            WHEN YM IN ('202403', '202406', '202407', '202408') AND 프로모션_구분 LIKE '%VIP%' AND 정산금액 IN (4000, 5000) THEN (((정산금액 - 1000) * 0.6) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END)) / 2
            WHEN YM IN ('202410', '202412', '202501', '202502') AND 프로모션_구분 LIKE '%VIP%' AND 정산금액 IN (3500, 4500) THEN (((정산금액 - 500) * 0.5) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END)) / 2
            WHEN YM IN ('202410', '202412', '202501', '202502') AND 프로모션_구분 LIKE '%VIP%' AND 정산금액 IN (4000, 5000) THEN (((정산금액 - 1000) * 0.5) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END)) / 2
        """
    }
}


_04_배민_부담금_기획전_브랜드찜 = {
    "main_web": {
        "queries1": """
            -- _04_배민_부담금_[기획전, 브랜드찜]
            (
                SELECT brand, '배민' AS 업체, 프로모션_구분 AS 프로모션,
                쿠폰사용금액 AS 금액, YM,
                CONCAT(DATE_FORMAT(MIN(사용일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(사용일자), '%m-%d')) AS 기간,
                0 AS 쿠폰건수,
                -1 * (
                    CASE
                        WHEN YM = '202406' AND 프로모션_구분 LIKE '%기획전(통합_2주)%' AND 쿠폰사용금액 IN (4500) THEN 1000 * COUNT(CASE WHEN 정산금액 != 0 THEN 1 END)
                        WHEN YM = '202502' AND 프로모션_구분 LIKE '%기획전(1~2월)%' AND 쿠폰사용금액 IN (5000) THEN 1000 * COUNT(CASE WHEN 정산금액 != 0 THEN 1 END)
                        WHEN 쿠폰사용금액 IN (3500, 4500) THEN 500 * COUNT(CASE WHEN 정산금액 != 0 THEN 1 END)
                        WHEN 쿠폰사용금액 IN (4000, 5000) THEN 1000 * COUNT(CASE WHEN 정산금액 != 0 THEN 1 END)
                        ELSE 0
                    END
                ) AS 합계
                FROM prom_baemin
                WHERE (YM = '202404' AND 프로모션_구분 LIKE '%브랜드찜%' AND 쿠폰사용금액 IN (3500))
                OR (YM = '202406' AND 프로모션_구분 LIKE '%기획전(통합_2주)%' AND 쿠폰사용금액 IN (4500))
                OR (YM = '202502' AND 프로모션_구분 LIKE '%기획전(1~2월)%' AND 쿠폰사용금액 IN (5000))
                GROUP BY brand, 업체, 프로모션, 금액, YM
            )
            UNION ALL\n
        """,
        "queries2": """
            -- _04_배민_부담금_[기획전, 브랜드찜]
            WHEN YM LIKE '%202404%' AND 프로모션_구분 LIKE '%브랜드찜%' AND (쿠폰사용금액 = 3500) THEN ((쿠폰사용금액 - 500) * 0.6) * (COUNT(CASE WHEN 정산금액 != 0 THEN 1 END))
            WHEN YM LIKE '%202406%' AND 프로모션_구분 LIKE '%기획전(통합_2주)%' AND (쿠폰사용금액 = 4500) THEN ((쿠폰사용금액 - 1000) * 0.6) * (COUNT(CASE WHEN 정산금액 != 0 THEN 1 END))
            WHEN YM LIKE '%202502%' AND 프로모션_구분 LIKE '%기획전(1~2월)%' AND (쿠폰사용금액 = 5000) THEN ((쿠폰사용금액 - 1000) * 0.6) * (COUNT(CASE WHEN 정산금액 != 0 THEN 1 END))
        """,
        "queries4": """
            -- _04_배민_부담금_[기획전, 브랜드찜]
            WHEN YM LIKE '%202404%' AND 프로모션_구분 LIKE '%브랜드찜%' AND (쿠폰사용금액 = 3500) THEN ((쿠폰사용금액 - 500) * 0.6) * (COUNT(CASE WHEN 정산금액 != 0 THEN 1 END))
            WHEN YM LIKE '%202406%' AND 프로모션_구분 LIKE '%기획전(통합_2주)%' AND (쿠폰사용금액 = 4500) THEN ((쿠폰사용금액 - 1000) * 0.6) * (COUNT(CASE WHEN 정산금액 != 0 THEN 1 END))
            WHEN YM LIKE '%202502%' AND 프로모션_구분 LIKE '%기획전(1~2월)%' AND (쿠폰사용금액 = 5000) THEN ((쿠폰사용금액 - 1000) * 0.6) * (COUNT(CASE WHEN 정산금액 != 0 THEN 1 END))
        """
    },
    "report_web": {
        "query1": """
            -- _04_배민_부담금_[기획전, 브랜드찜]
            SELECT
                YM,
                brand,
                프로모션_구분,
                CONCAT(DATE_FORMAT(MIN(사용일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(사용일자), '%m-%d')) AS 기간,
                '-' AS 쿠폰건수,
                SUM(CASE 
                        WHEN YM = '202406' AND 프로모션_구분 LIKE '%기획전(통합_2주)%' AND 쿠폰사용금액 IN (4500) THEN -1 * 1000 * 0.4 
                        WHEN YM = '202502' AND 프로모션_구분 LIKE '%기획전(1~2월)%' AND 쿠폰사용금액 IN (5000) THEN -1 * 1000 * 0.5 
                        WHEN ((YM >= '202401' AND YM <= '202408') OR (YM = '202409' AND MONTH(사용일자) = 8)) AND 쿠폰사용금액 IN (3500, 4500) THEN -1 * 500 * 0.4 
                        WHEN ((YM >= '202401' AND YM <= '202408') OR (YM = '202409' AND MONTH(사용일자) = 8)) AND 쿠폰사용금액 IN (4000, 5000) THEN -1 * 1000 * 0.4 
                        WHEN YM >= '202409' AND 쿠폰사용금액 IN (3500, 4500) THEN -1 * 500 * 0.5
                        WHEN YM >= '202409' AND 쿠폰사용금액 IN (4000, 5000) THEN -1 * 1000 * 0.5
                        ELSE 0
                    END) AS 본사분담금,
                SUM(CASE 
                        WHEN YM = '202406' AND 프로모션_구분 LIKE '%기획전(통합_2주)%' AND 쿠폰사용금액 IN (4500) THEN -1 * 1000 * 0.6 
                        WHEN YM = '202502' AND 프로모션_구분 LIKE '%기획전(1~2월)%' AND 쿠폰사용금액 IN (5000) THEN -1 * 1000 * 0.5 
                        WHEN ((YM >= '202401' AND YM <= '202408') OR (YM = '202409' AND MONTH(사용일자) = 8)) AND 쿠폰사용금액 IN (3500, 4500) THEN -1 * 500 * 0.6 
                        WHEN ((YM >= '202401' AND YM <= '202408') OR (YM = '202409' AND MONTH(사용일자) = 8)) AND 쿠폰사용금액 IN (4000, 5000) THEN -1 * 1000 * 0.6 
                        WHEN YM >= '202409' AND 쿠폰사용금액 IN (3500, 4500) THEN -1 * 500 * 0.5
                        WHEN YM >= '202409' AND 쿠폰사용금액 IN (4000, 5000) THEN -1 * 1000 * 0.5
                        ELSE 0
                    END) AS 가맹점분담금,
                '' AS 광고분담금,
                SUM(CASE 
                        WHEN YM = '202406' AND 프로모션_구분 LIKE '%기획전(통합_2주)%' AND 쿠폰사용금액 IN (4500) THEN -1 * 1000
                        WHEN YM = '202502' AND 프로모션_구분 LIKE '%기획전(1~2월)%' AND 쿠폰사용금액 IN (5000) THEN -1 * 1000
                        WHEN 쿠폰사용금액 IN (3500, 4500) THEN -1 * 500
                        WHEN 쿠폰사용금액 IN (4000, 5000) THEN -1 * 1000
                        ELSE 0
                    END) AS 합계
            FROM prom_baemin
            WHERE 
                YM = '202404' AND 프로모션_구분 LIKE '%브랜드찜%' AND 쿠폰사용금액 IN (3500) 
                OR
                YM = '202406' AND 프로모션_구분 LIKE '%기획전(통합_2주)%' AND 쿠폰사용금액 IN (4500) 
                OR
                YM = '202502' AND 프로모션_구분 LIKE '%기획전(1~2월)%' AND 쿠폰사용금액 IN (5000) 
            GROUP BY YM, brand, 프로모션_구분
            UNION ALL\n
        """,
        "query2": """
            -- 배민 부담금04 [기획전]
            SELECT
                YM,
                brand,
                프로모션_구분 AS 내용,
                CONCAT(DATE_FORMAT(MIN(사용일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(사용일자), '%m-%d')) AS 날짜,
                쿠폰사용금액 AS 금액,
                '-' AS 쿠폰건수_전체,
                SUM(CASE 
                        WHEN YM = '202406' AND 프로모션_구분 LIKE '%기획전(통합_2주)%' AND 쿠폰사용금액 IN (4500) THEN -1 * 1000
                        WHEN YM = '202502' AND 프로모션_구분 LIKE '%기획전(1~2월)%' AND 쿠폰사용금액 IN (5000) THEN -1 * 1000
                        WHEN 쿠폰사용금액 IN (3500, 4500) THEN -1 * 500
                        WHEN 쿠폰사용금액 IN (4000, 5000) THEN -1 * 1000
                        ELSE 0
                    END) AS 납부금액_전체,
                CASE 
                    WHEN YM = '202406' AND 프로모션_구분 LIKE '%기획전(통합_2주)%' AND 쿠폰사용금액 IN (4500) THEN (쿠폰사용금액 - 1000) * 0.4 
                    WHEN YM = '202502' AND 프로모션_구분 LIKE '%기획전(1~2월)%' AND 쿠폰사용금액 IN (5000) THEN (쿠폰사용금액 - 1000) * 0.5 
                    WHEN ((YM >= '202401' AND YM <= '202408') OR (YM = '202409' AND MONTH(사용일자) = 8)) AND 쿠폰사용금액 IN (3500, 4500) THEN (쿠폰사용금액 - 500) * 0.4 
                    WHEN ((YM >= '202401' AND YM <= '202408') OR (YM = '202409' AND MONTH(사용일자) = 8)) AND 쿠폰사용금액 IN (4000, 5000) THEN (쿠폰사용금액 - 1000) * 0.4 
                    WHEN YM >= '202409' AND 쿠폰사용금액 IN (3500, 4500) THEN -1 * 500 * 0.5
                    WHEN YM >= '202409' AND 쿠폰사용금액 IN (4000, 5000) THEN -1 * 1000 * 0.5
                    ELSE 0
                END AS 분담액_본사,
                SUM(CASE 
                        WHEN YM = '202406' AND 프로모션_구분 LIKE '%기획전(통합_2주)%' AND 쿠폰사용금액 IN (4500) THEN -1 * 1000 * 0.4 
                        WHEN YM = '202502' AND 프로모션_구분 LIKE '%기획전(1~2월)%' AND 쿠폰사용금액 IN (5000) THEN -1 * 1000 * 0.5 
                        WHEN ((YM >= '202401' AND YM <= '202408') OR (YM = '202409' AND MONTH(사용일자) = 8)) AND 쿠폰사용금액 IN (3500, 4500) THEN -1 * 500 * 0.4 
                        WHEN ((YM >= '202401' AND YM <= '202408') OR (YM = '202409' AND MONTH(사용일자) = 8)) AND 쿠폰사용금액 IN (4000, 5000) THEN -1 * 1000 * 0.4 
                        WHEN YM >= '202409' AND 쿠폰사용금액 IN (3500, 4500) THEN -1 * 500 * 0.5
                        WHEN YM >= '202409' AND 쿠폰사용금액 IN (4000, 5000) THEN -1 * 1000 * 0.5
                        ELSE 0
                    END) AS 본사_분담액,
                CASE 
                    WHEN YM = '202406' AND 프로모션_구분 LIKE '%기획전(통합_2주)%' AND 쿠폰사용금액 IN (4500) THEN (쿠폰사용금액 - 1000) * 0.6
                    WHEN YM = '202502' AND 프로모션_구분 LIKE '%기획전(1~2월)%' AND 쿠폰사용금액 IN (5000) THEN (쿠폰사용금액 - 1000) * 0.5
                    WHEN ((YM >= '202401' AND YM <= '202408') OR (YM = '202409' AND MONTH(사용일자) = 8)) AND 쿠폰사용금액 IN (3500, 4500) THEN (쿠폰사용금액 - 500) * 0.6
                    WHEN ((YM >= '202401' AND YM <= '202408') OR (YM = '202409' AND MONTH(사용일자) = 8)) AND 쿠폰사용금액 IN (4000, 5000) THEN (쿠폰사용금액 - 1000) * 0.6
                    WHEN YM >= '202409' AND 쿠폰사용금액 IN (3500, 4500) THEN -1 * 500 * 0.5
                    WHEN YM >= '202409' AND 쿠폰사용금액 IN (4000, 5000) THEN -1 * 1000 * 0.5
                    ELSE 0
                END AS 분담액_가맹,
                SUM(CASE 
                        WHEN YM = '202406' AND 프로모션_구분 LIKE '%기획전(통합_2주)%' AND 쿠폰사용금액 IN (4500) THEN -1 * 1000 * 0.6
                        WHEN YM = '202502' AND 프로모션_구분 LIKE '%기획전(1~2월)%' AND 쿠폰사용금액 IN (5000) THEN -1 * 1000 * 0.5
                        WHEN ((YM >= '202401' AND YM <= '202408') OR (YM = '202409' AND MONTH(사용일자) = 8)) AND 쿠폰사용금액 IN (3500, 4500) THEN -1 * 500 * 0.6 
                        WHEN ((YM >= '202401' AND YM <= '202408') OR (YM = '202409' AND MONTH(사용일자) = 8)) AND 쿠폰사용금액 IN (4000, 5000) THEN -1 * 1000 * 0.6 
                        WHEN YM >= '202409' AND 쿠폰사용금액 IN (3500, 4500) THEN -1 * 500 * 0.5
                        WHEN YM >= '202409' AND 쿠폰사용금액 IN (4000, 5000) THEN -1 * 1000 * 0.5
                        ELSE 0
                    END) AS 합계_가맹,
                '' AS 분담액,
                '' AS 지원금액
            FROM prom_baemin
            WHERE 
                YM = '202404' AND 프로모션_구분 LIKE '%브랜드찜%' AND 쿠폰사용금액 IN (3500) 
                OR
                YM = '202406' AND 프로모션_구분 LIKE '%기획전(통합_2주)%' AND 쿠폰사용금액 IN (4500) 
                OR
                YM = '202502' AND 프로모션_구분 LIKE '%기획전(1~2월)%' AND 쿠폰사용금액 IN (5000) 
            GROUP BY YM, brand, 내용, 금액, 사용일자
            UNION ALL\n
        """
    },
    "shop_detail": {
        "분담금": """
            -- _04_배민_부담금_[기획전, 브랜드찜]
            WHEN YM = '202404' AND 프로모션_구분 LIKE '%브랜드찜%' AND 정산금액 = 3500 THEN ROUND(((정산금액 - 500) * 0.6), 1)
            WHEN YM = '202406' AND 프로모션_구분 LIKE '%기획전(통합_2주)%' AND 정산금액 = 4500 THEN ROUND(((정산금액 - 1000) * 0.6), 1)
            WHEN YM = '202502' AND 프로모션_구분 LIKE '%기획전(1~2월)%' AND 정산금액 = 5000 THEN ROUND(((정산금액 - 1000) * 0.5), 1)
        """,
        "총합계": """
            -- _04_배민_부담금_[기획전, 브랜드찜]
            WHEN YM = '202404' AND 프로모션_구분 LIKE '%브랜드찜%' AND 정산금액 = 3500 THEN ((정산금액 - 500) * 0.6) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END)
            WHEN YM = '202406' AND 프로모션_구분 LIKE '%기획전(통합_2주)%' AND 정산금액 = 4500 THEN SUM(쿠폰사용금액 - 1000) * 0.6
            WHEN YM = '202502' AND 프로모션_구분 LIKE '%기획전(1~2월)%' AND 정산금액 = 5000 THEN SUM(쿠폰사용금액 - 1000) * 0.5
        """,
        "과금1차": """
            -- _04_배민_부담금_[기획전, 브랜드찜]
            WHEN YM = '202404' AND 프로모션_구분 LIKE '%브랜드찜%' AND 정산금액 = 3500 THEN (((정산금액 - 500) * 0.6) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END)) / 2
            WHEN YM = '202406' AND 프로모션_구분 LIKE '%기획전(통합_2주)%' AND 정산금액 = 4500 THEN (SUM(쿠폰사용금액 - 1000) * 0.6) / 2
            WHEN YM = '202502' AND 프로모션_구분 LIKE '%기획전(1~2월)%' AND 정산금액 = 5000 THEN (SUM(쿠폰사용금액 - 1000) * 0.5) / 2
        """,
        "과금2차": """
            -- _04_배민_부담금_[기획전, 브랜드찜]
            WHEN YM = '202404' AND 프로모션_구분 LIKE '%브랜드찜%' AND 정산금액 = 3500 THEN (((정산금액 - 500) * 0.6) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END)) / 2
            WHEN YM = '202406' AND 프로모션_구분 LIKE '%기획전(통합_2주)%' AND 정산금액 = 4500 THEN (SUM(쿠폰사용금액 - 1000) * 0.6) / 2
            WHEN YM = '202502' AND 프로모션_구분 LIKE '%기획전(1~2월)%' AND 정산금액 = 5000 THEN (SUM(쿠폰사용금액 - 1000) * 0.5) / 2
        """
    }
}


_05_배민_부담금_네이버페이 = {
    "main_web": {
        "queries1": """
            -- _05_배민_부담금_[네이버페이]
            (
                SELECT
                    brand,
                    '배민' AS 업체,
                    프로모션_구분 AS 프로모션,
                    쿠폰사용금액 AS 금액,
                    YM,
                    CONCAT(DATE_FORMAT(MIN(사용일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(사용일자), '%m-%d')) AS 기간,
                    0 AS 쿠폰건수,
                    -1 * (
                        CASE
                            WHEN YM = '202407' AND 프로모션_구분 LIKE '%네이버페이%' AND 쿠폰사용금액 IN (5000) 
                            THEN 2000 * COUNT(CASE WHEN 정산금액 != 0 THEN 1 END)
                            ELSE 0
                        END
                    ) AS 합계
                FROM
                    prom_baemin
                WHERE
                    YM = '202407' AND 프로모션_구분 LIKE '%네이버페이%' AND 쿠폰사용금액 IN (5000)
                GROUP BY
                    brand, 업체, 프로모션, 금액, YM
            )
            UNION ALL\n
        """,
        "queries2": """
            -- _05_배민_부담금_[네이버페이]
            WHEN YM LIKE '%202407%' AND 프로모션_구분 LIKE '%네이버페이%' AND (쿠폰사용금액 = 5000) THEN ((쿠폰사용금액 - 2000) * 0.6) * (COUNT(CASE WHEN 정산금액 != 0 THEN 1 END))
        """,
        "queries4": """
            -- _05_배민_부담금_[네이버페이]
            WHEN YM LIKE '%202407%' AND 프로모션_구분 LIKE '%네이버페이%' AND (쿠폰사용금액 = 5000) THEN ((쿠폰사용금액 - 2000) * 0.6) * (COUNT(CASE WHEN 정산금액 != 0 THEN 1 END))
        """
    },
    "report_web": {
        "query1": """
            -- _05_배민_부담금_[네이버페이]
            SELECT
                YM,
                brand,
                프로모션_구분,
                CONCAT(DATE_FORMAT(MIN(사용일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(사용일자), '%m-%d')) AS 기간,
                '-' AS 쿠폰건수,
                SUM(CASE 
                        WHEN YM = '202407' AND 프로모션_구분 LIKE '%네이버페이%' AND 쿠폰사용금액 IN (5000) THEN -1 * 2000 * 0.4 
                        ELSE 0
                    END) AS 본사분담금,
                SUM(CASE 
                        WHEN YM = '202407' AND 프로모션_구분 LIKE '%네이버페이%' AND 쿠폰사용금액 IN (5000) THEN -1 * 2000 * 0.6 
                        ELSE 0
                    END) AS 가맹점분담금,
                '' AS 광고분담금,
                SUM(CASE 
                        WHEN YM = '202407' AND 프로모션_구분 LIKE '%네이버페이%' AND 쿠폰사용금액 IN (5000) THEN -1 * 2000
                        ELSE 0
                    END) AS 합계
            FROM prom_baemin
            WHERE 
                YM = '202407' AND 프로모션_구분 LIKE '%네이버페이%' AND 쿠폰사용금액 IN (5000) 
            GROUP BY YM, brand, 프로모션_구분
            UNION ALL\n    
        """,
        "query2": """
            -- _05_배민_부담금_[네이버페이]
            SELECT
                YM,
                brand,
                프로모션_구분 AS 내용,
                CONCAT(DATE_FORMAT(MIN(사용일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(사용일자), '%m-%d')) AS 날짜,
                쿠폰사용금액 AS 금액,
                '-' AS 쿠폰건수_전체,
                SUM(CASE 
                        WHEN YM = '202407' AND 프로모션_구분 LIKE '%네이버페이%' AND 쿠폰사용금액 IN (5000) THEN -1 * 2000
                        ELSE 0
                    END) AS 납부금액_전체,
                CASE 
                    WHEN YM = '202407' AND 프로모션_구분 LIKE '%네이버페이%' AND 쿠폰사용금액 IN (5000) THEN (쿠폰사용금액 - 2000) * 0.4 
                    ELSE 0
                END AS 분담액_본사,
                SUM(CASE 
                        WHEN YM = '202407' AND 프로모션_구분 LIKE '%네이버페이%' AND 쿠폰사용금액 IN (5000) THEN -1 * 2000 * 0.4 
                        ELSE 0
                    END) AS 본사_분담액,
                CASE 
                    WHEN YM = '202407' AND 프로모션_구분 LIKE '%네이버페이%' AND 쿠폰사용금액 IN (5000) THEN (쿠폰사용금액 - 2000) * 0.6
                    ELSE 0
                END AS 분담액_가맹,
                SUM(CASE 
                        WHEN YM = '202407' AND 프로모션_구분 LIKE '%네이버페이%' AND 쿠폰사용금액 IN (5000) THEN -1 * 2000 * 0.6
                        ELSE 0
                    END) AS 합계_가맹,
                '' AS 분담액,
                '' AS 지원금액
            FROM prom_baemin
            WHERE 
                YM = '202407' AND 프로모션_구분 LIKE '%네이버페이%' AND 쿠폰사용금액 IN (5000) 
            GROUP BY YM, brand, 내용, 금액
            UNION ALL\n
        """
    },
    "shop_detail": {
        "분담금": """
            -- _05_배민_부담금_[네이버페이]
            WHEN YM = '202407' AND 프로모션_구분 LIKE '%네이버페이%' AND 정산금액 = 5000 THEN ROUND(((정산금액 - 2000) * 0.6), 1)
        """,
        "총합계": """
            -- _05_배민_부담금_[네이버페이]
            WHEN YM = '202407' AND 프로모션_구분 LIKE '%네이버페이%' AND 정산금액 = 5000 THEN SUM(쿠폰사용금액 - 2000) * 0.6
        """,
        "과금1차": """
            -- _05_배민_부담금_[네이버페이]
            WHEN YM = '202407' AND 프로모션_구분 LIKE '%네이버페이%' AND 정산금액 = 5000 THEN (SUM(쿠폰사용금액 - 2000) * 0.6) / 2
        """,
        "과금2차": """
            -- _05_배민_부담금_[네이버페이]
            WHEN YM = '202407' AND 프로모션_구분 LIKE '%네이버페이%' AND 정산금액 = 5000 THEN (SUM(쿠폰사용금액 - 2000) * 0.6) / 2
        """
    }
}


_06_배민_부담금_KT달달 = {
    "main_web": {
        "queries1": """
            -- _06_배민_부담금_[KT달달]
            (
                SELECT
                    brand,
                    '배민' AS 업체,
                    프로모션_구분 AS 프로모션,
                    쿠폰사용금액 AS 금액,
                    YM,
                    CONCAT(DATE_FORMAT(MIN(사용일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(사용일자), '%m-%d')) AS 기간,
                    0 AS 쿠폰건수,
                    -1 * (
                        CASE
                            WHEN YM = '202411' AND 프로모션_구분 LIKE '%KT달달%' 
                            THEN 2000 * COUNT(CASE WHEN 정산금액 != 0 THEN 1 END)
                            ELSE 0
                        END
                    ) AS 합계
                FROM
                    prom_baemin
                WHERE
                    YM = '202411' AND 프로모션_구분 LIKE '%KT달달%'
                GROUP BY
                    brand, 업체, 프로모션, 금액, YM
            )
            UNION ALL\n
        """,
        "queries2": """
            -- _06_배민_부담금_[KT달달]
            WHEN YM IN ('202411') AND 프로모션_구분 LIKE '%KT달달%' THEN ((쿠폰사용금액 - 2000) * 0.5) * (COUNT(CASE WHEN 정산금액 != 0 THEN 1 END))
        """,
        "queries4": """
            -- _06_배민_부담금_[KT달달]
            WHEN YM IN ('202411') AND 프로모션_구분 LIKE '%KT달달%' THEN ((쿠폰사용금액 - 2000) * 0.5) * (COUNT(CASE WHEN 정산금액 != 0 THEN 1 END))
        """
    },
    "report_web": {
        "query1": """
            -- _06_배민_부담금_[KT달달]
            SELECT
                YM,
                brand,
                프로모션_구분,
                CONCAT(DATE_FORMAT(MIN(사용일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(사용일자), '%m-%d')) AS 기간,
                '-' AS 쿠폰건수,
                SUM(CASE 
                        WHEN YM = '202411' AND 프로모션_구분 LIKE '%KT달달%' THEN -1 * 2000 * 0.5
                        ELSE 0
                    END) AS 본사분담금,
                SUM(CASE 
                        WHEN YM = '202411' AND 프로모션_구분 LIKE '%KT달달%' THEN -1 * 2000 * 0.5
                        ELSE 0
                    END) AS 가맹점분담금,
                '' AS 광고분담금,
                SUM(CASE 
                        WHEN YM = '202411' AND 프로모션_구분 LIKE '%KT달달%' THEN -1 * 2000
                        ELSE 0
                    END) AS 합계
            FROM prom_baemin
            WHERE 
                YM = '202411' AND 프로모션_구분 LIKE '%KT달달%'
            GROUP BY YM, brand, 프로모션_구분
            UNION ALL\n    
        """,
        "query2": """
            -- _06_배민_부담금_[KT달달]
                SELECT
                    YM,
                    brand,
                    프로모션_구분 AS 내용,
                    CONCAT(DATE_FORMAT(MIN(사용일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(사용일자), '%m-%d')) AS 날짜,
                    쿠폰사용금액 AS 금액,
                    '-' AS 쿠폰건수_전체,
                    SUM(CASE 
                            WHEN YM = '202411' AND 프로모션_구분 LIKE '%KT달달%' THEN -1 * 2000
                            ELSE 0
                        END) AS 납부금액_전체,
                    CASE 
                        WHEN YM = '202411' AND 프로모션_구분 LIKE '%KT달달%' THEN (-2000) * 0.5
                        ELSE 0
                    END AS 분담액_본사,
                    SUM(CASE 
                            WHEN YM = '202411' AND 프로모션_구분 LIKE '%KT달달%' THEN -1 * 2000 * 0.5
                            ELSE 0
                        END) AS 본사_분담액,
                    CASE 
                        WHEN YM = '202411' AND 프로모션_구분 LIKE '%KT달달%' THEN (-2000) * 0.5
                        ELSE 0
                    END AS 분담액_가맹,
                    SUM(CASE 
                            WHEN YM = '202411' AND 프로모션_구분 LIKE '%KT달달%' THEN -1 * 2000 * 0.5
                            ELSE 0
                        END) AS 합계_가맹,
                    '' AS 분담액,
                    '' AS 지원금액
                FROM prom_baemin
                WHERE 
                    YM = '202411' AND 프로모션_구분 LIKE '%KT달달%'
                GROUP BY YM, brand, 내용, 금액
                UNION ALL\n
        """
    },
    "shop_detail": {
        "분담금": """
            -- _06_배민_부담금_[KT달달]
            WHEN YM IN ('202411') AND 프로모션_구분 LIKE '%KT달달%' THEN ROUND(((정산금액 - 2000) * 0.5), 1)
        """,
        "총합계": """
            -- _06_배민_부담금_[KT달달]
            WHEN YM IN ('202411') AND 프로모션_구분 LIKE '%KT달달%' THEN ((정산금액 - 2000) * 0.5) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END)
        """,
        "과금1차": """
            -- _06_배민_부담금_[KT달달]
            WHEN YM IN ('202411') AND 프로모션_구분 LIKE '%KT달달%' THEN ((정산금액 - 2000) * 0.5) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END) / 2
        """,
        "과금2차": """
            -- _06_배민_부담금_[KT달달]
            WHEN YM IN ('202411') AND 프로모션_구분 LIKE '%KT달달%' THEN ((정산금액 - 2000) * 0.5) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END) / 2
        """
    }
}


_07_배민_부담금_HVA = {
    "main_web": {
        "queries1": """
            -- _07_배민_부담금_[HVA]
            (
                SELECT
                    brand,
                    '배민' AS 업체,
                    프로모션_구분 AS 프로모션,
                    쿠폰사용금액 AS 금액,
                    YM,
                    CONCAT(DATE_FORMAT(MIN(사용일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(사용일자), '%m-%d')) AS 기간,
                    0 AS 쿠폰건수,
                    -1 * (
                        CASE
                            WHEN 프로모션_구분 LIKE 'HVA4%' AND 쿠폰사용금액 != 4000 THEN (쿠폰사용금액 - 4000) * COUNT(CASE WHEN 정산금액 != 0 THEN 1 END)
                            WHEN 프로모션_구분 LIKE 'HVA%' AND 프로모션_구분 NOT LIKE 'HVA4%' AND 쿠폰사용금액 != 3000 THEN (쿠폰사용금액 - 3000) * COUNT(CASE WHEN 정산금액 != 0 THEN 1 END)
                            ELSE 0
                        END
                    ) AS 합계
                FROM
                    prom_baemin
                WHERE
                    YM >= '202411' AND 프로모션_구분 LIKE 'HVA%'
                GROUP BY
                    brand, 업체, 프로모션, 금액, YM
            )
            UNION ALL\n
        """,
        "queries2": """
            -- _07_배민_부담금_[HVA]
            WHEN YM IN ('202411', '202412', '202501', '202502') AND 프로모션_구분 LIKE 'HVA4%' AND (쿠폰사용금액 != 4000) THEN ((4000) * 0.5) * (COUNT(CASE WHEN 정산금액 != 0 THEN 1 END))
            WHEN YM IN ('202411', '202412', '202501', '202502') AND 프로모션_구분 LIKE 'HVA%' AND 프로모션_구분 NOT LIKE 'HVA4%' AND (쿠폰사용금액 != 3000) THEN ((3000) * 0.5) * (COUNT(CASE WHEN 정산금액 != 0 THEN 1 END))
        """,
        "queries4": """
            -- _07_배민_부담금_[HVA]
            WHEN YM IN ('202411', '202412', '202501', '202502') AND 프로모션_구분 LIKE 'HVA4%' AND (쿠폰사용금액 != 4000) THEN ((4000) * 0.5) * (COUNT(CASE WHEN 정산금액 != 0 THEN 1 END))
            WHEN YM IN ('202411', '202412', '202501', '202502') AND 프로모션_구분 LIKE 'HVA%' AND 프로모션_구분 NOT LIKE 'HVA4%' AND (쿠폰사용금액 != 3000) THEN ((3000) * 0.5) * (COUNT(CASE WHEN 정산금액 != 0 THEN 1 END))
        """
    },
    "report_web": {
        "query1": """
            -- _07_배민_부담금_[HVA]
            SELECT
                YM,
                brand,
                프로모션_구분,
                CONCAT(DATE_FORMAT(MIN(사용일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(사용일자), '%m-%d')) AS 기간,
                '-' AS 쿠폰건수,
                SUM(CASE 
                        WHEN 프로모션_구분 LIKE 'HVA4%' AND 쿠폰사용금액 != 4000 THEN -1 * (쿠폰사용금액 - 4000) * 0.5
                        WHEN 프로모션_구분 LIKE 'HVA%' AND 프로모션_구분 NOT LIKE 'HVA4%' AND 쿠폰사용금액 != 3000 THEN -1 * (쿠폰사용금액 - 3000) * 0.5
                        ELSE 0
                    END) AS 본사분담금,
                SUM(CASE 
                        WHEN 프로모션_구분 LIKE 'HVA4%' AND 쿠폰사용금액 != 4000 THEN -1 * (쿠폰사용금액 - 4000) * 0.5
                        WHEN 프로모션_구분 LIKE 'HVA%' AND 프로모션_구분 NOT LIKE 'HVA4%' AND 쿠폰사용금액 != 3000 THEN -1 * (쿠폰사용금액 - 3000) * 0.5
                        ELSE 0
                    END) AS 가맹점분담금,
                '' AS 광고분담금,
                SUM(CASE 
                        WHEN 프로모션_구분 LIKE 'HVA4%' AND 쿠폰사용금액 != 4000 THEN -1 * (쿠폰사용금액 - 4000)
                        WHEN 프로모션_구분 LIKE 'HVA%' AND 프로모션_구분 NOT LIKE 'HVA4%' AND 쿠폰사용금액 != 3000 THEN -1 * (쿠폰사용금액 - 3000)
                        ELSE 0
                    END) AS 합계
            FROM prom_baemin
            WHERE 
                (YM >= '202411') AND 프로모션_구분 LIKE 'HVA%'
            GROUP BY YM, brand, 프로모션_구분
            UNION ALL\n    
        """,
        "query2": """
            -- _07_배민_부담금_[HVA]
            SELECT
                YM,
                brand,
                프로모션_구분 AS 내용,
                CONCAT(DATE_FORMAT(MIN(사용일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(사용일자), '%m-%d')) AS 날짜,
                쿠폰사용금액 AS 금액,
                '-' AS 쿠폰건수_전체,
                SUM(CASE 
                        WHEN 프로모션_구분 LIKE 'HVA4%' THEN -1 * (쿠폰사용금액 - 4000)
                        WHEN 프로모션_구분 LIKE 'HVA%' AND 프로모션_구분 NOT LIKE 'HVA4%' THEN -1 * (쿠폰사용금액 - 3000)
                        ELSE 0
                    END) AS 납부금액_전체,
                CASE 
                    WHEN 프로모션_구분 LIKE 'HVA4%' THEN -1 * (쿠폰사용금액 - 4000) * 0.5
                    WHEN 프로모션_구분 LIKE 'HVA%' AND 프로모션_구분 NOT LIKE 'HVA4%' THEN -1 * (쿠폰사용금액 - 3000) * 0.5
                    ELSE 0
                END AS 분담액_본사,
                SUM(CASE 
                        WHEN 프로모션_구분 LIKE 'HVA4%' THEN -1 * (쿠폰사용금액 - 4000) * 0.5
                        WHEN 프로모션_구분 LIKE 'HVA%' AND 프로모션_구분 NOT LIKE 'HVA4%' THEN -1 * (쿠폰사용금액 - 3000) * 0.5
                        ELSE 0
                    END) AS 본사_분담액,
                CASE 
                    WHEN 프로모션_구분 LIKE 'HVA4%' THEN -1 * (쿠폰사용금액 - 4000) * 0.5
                    WHEN 프로모션_구분 LIKE 'HVA%' AND 프로모션_구분 NOT LIKE 'HVA4%' THEN -1 * (쿠폰사용금액 - 3000) * 0.5
                    ELSE 0
                END AS 분담액_가맹,
                SUM(CASE 
                        WHEN 프로모션_구분 LIKE 'HVA4%' THEN -1 * (쿠폰사용금액 - 4000) * 0.5
                        WHEN 프로모션_구분 LIKE 'HVA%' AND 프로모션_구분 NOT LIKE 'HVA4%' THEN -1 * (쿠폰사용금액 - 3000) * 0.5
                        ELSE 0
                    END) AS 합계_가맹,
                '' AS 분담액,
                '' AS 지원금액
            FROM prom_baemin
            WHERE 
                (YM >= '202411') AND 프로모션_구분 LIKE 'HVA%'
            GROUP BY YM, brand, 내용, 금액
            UNION ALL\n
        """
    },
    "shop_detail": {
        "분담금": """
            -- _07_배민_부담금_[HVA]
            WHEN YM IN ('202411', '202412', '202501', '202502') AND 프로모션_구분 LIKE 'HVA4%' AND (정산금액 != 4000) THEN ROUND(((4000) * 0.5), 1)
            WHEN YM IN ('202411', '202412', '202501', '202502') AND 프로모션_구분 LIKE 'HVA%' AND 프로모션_구분 NOT LIKE 'HVA4%' AND (정산금액 != 3000) THEN ROUND(((3000) * 0.5), 1)
        """,
        "총합계": """
            -- _07_배민_부담금_[HVA]
            WHEN YM IN ('202411', '202412', '202501', '202502') AND 프로모션_구분 LIKE 'HVA4%' AND (정산금액 != 4000) THEN ((4000) * 0.5) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END)
            WHEN YM IN ('202411', '202412', '202501', '202502') AND 프로모션_구분 LIKE 'HVA%' AND 프로모션_구분 NOT LIKE 'HVA4%' AND (정산금액 != 3000) THEN ((3000) * 0.5) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END)
        """,
        "과금1차": """
            -- _07_배민_부담금_[HVA]
            WHEN YM IN ('202411', '202412', '202501', '202502') AND 프로모션_구분 LIKE 'HVA4%' AND (정산금액 != 4000) THEN ((4000) * 0.5) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END) / 2
            WHEN YM IN ('202411', '202412', '202501', '202502') AND 프로모션_구분 LIKE 'HVA%' AND 프로모션_구분 NOT LIKE 'HVA4%' AND (정산금액 != 3000) THEN ((3000) * 0.5) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END) / 2
        """,
        "과금2차": """
            -- _07_배민_부담금_[HVA]
            WHEN YM IN ('202411', '202412', '202501', '202502') AND 프로모션_구분 LIKE 'HVA4%' AND (정산금액 != 4000) THEN ((4000) * 0.5) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END) / 2
            WHEN YM IN ('202411', '202412', '202501', '202502') AND 프로모션_구분 LIKE 'HVA%' AND 프로모션_구분 NOT LIKE 'HVA4%' AND (정산금액 != 3000) THEN ((3000) * 0.5) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END) / 2
        """
    }
}


_08_배민_부담금_코카콜라_숯불 = {
    "main_web": {
        "queries1": """
            -- _08_배민_부담금_[코카콜라.숯불]
            (
                SELECT
                    brand,
                    '배민' AS 업체,
                    프로모션_구분 AS 프로모션,
                    쿠폰사용금액 AS 금액,
                    YM,
                    CONCAT(DATE_FORMAT(MIN(사용일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(사용일자), '%m-%d')) AS 기간,
                    0 AS 쿠폰건수,
                    -1 * (
                        CASE
                            WHEN YM = '202411' AND brand = '숯불' AND 프로모션_구분 LIKE '%코카콜라%' AND 쿠폰사용금액 IN (4000) THEN 1000 * COUNT(CASE WHEN 정산금액 != 0 THEN 1 END)
                            ELSE 0
                        END
                    ) AS 합계
                FROM
                    prom_baemin
                WHERE
                    YM = '202411' AND brand = '숯불' AND 프로모션_구분 LIKE '%코카콜라%' AND 쿠폰사용금액 IN (4000)
                GROUP BY
                    brand, 업체, 프로모션, 금액, YM
            )
            UNION ALL\n
        """,
        "queries2": """
            -- _08_배민_부담금_[코카콜라.숯불]
            WHEN YM IN ('202411') AND brand = '숯불' AND 프로모션_구분 LIKE '%코카콜라%' AND (쿠폰사용금액 = 4000) THEN ((쿠폰사용금액 - 1000) * 0.5) * (COUNT(CASE WHEN 정산금액 != 0 THEN 1 END))
        """,
        "queries4": """
            -- _08_배민_부담금_[코카콜라.숯불]
            WHEN YM IN ('202411') AND brand = '숯불' AND 프로모션_구분 LIKE '%코카콜라%' AND (쿠폰사용금액 = 4000) THEN ((쿠폰사용금액 - 1000) * 0.5) * (COUNT(CASE WHEN 정산금액 != 0 THEN 1 END))
        """
    },
    "report_web": {
        "query1": """
            -- _08_배민_부담금_[코카콜라.숯불]
            SELECT
                YM,
                brand,
                프로모션_구분,
                CONCAT(DATE_FORMAT(MIN(사용일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(사용일자), '%m-%d')) AS 기간,
                '-' AS 쿠폰건수,
                SUM(CASE 
                        WHEN YM = '202411' AND brand = "숯불" AND 프로모션_구분 LIKE '%코카콜라%' AND 쿠폰사용금액 IN (4000) THEN -1 * 1000 * 0.5
                        ELSE 0
                    END) AS 본사분담금,
                SUM(CASE 
                        WHEN YM = '202411' AND brand = "숯불" AND 프로모션_구분 LIKE '%코카콜라%' AND 쿠폰사용금액 IN (4000) THEN -1 * 1000 * 0.5
                        ELSE 0
                    END) AS 가맹점분담금,
                '' AS 광고분담금,
                SUM(CASE 
                        WHEN YM = '202411' AND brand = "숯불" AND 프로모션_구분 LIKE '%코카콜라%' AND 쿠폰사용금액 IN (4000) THEN -1 * 1000
                        ELSE 0
                    END) AS 합계
            FROM prom_baemin
            WHERE
                YM = '202411' AND brand = "숯불" AND 프로모션_구분 LIKE '%코카콜라%' AND 쿠폰사용금액 IN (4000)
            GROUP BY YM, brand, 프로모션_구분
            UNION ALL\n    
        """,
        "query2": """
            -- _08_배민_부담금_[코카콜라.숯불]
            SELECT
                YM,
                brand,
                프로모션_구분 AS 내용,
                CONCAT(DATE_FORMAT(MIN(사용일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(사용일자), '%m-%d')) AS 날짜,
                쿠폰사용금액 AS 금액,
                '-' AS 쿠폰건수_전체,
                SUM(CASE 
                        WHEN YM = '202411' AND brand = "숯불" AND 프로모션_구분 LIKE '%코카콜라%' AND 쿠폰사용금액 = 4000 THEN -1 * 1000
                        ELSE 0
                    END) AS 납부금액_전체,
                CASE 
                    WHEN YM = '202411' AND brand = "숯불" AND 프로모션_구분 LIKE '%코카콜라%' AND 쿠폰사용금액 = 4000 THEN (-1000) * 0.5
                    ELSE 0
                END AS 분담액_본사,
                SUM(CASE 
                        WHEN YM = '202411' AND brand = "숯불" AND 프로모션_구분 LIKE '%코카콜라%' AND 쿠폰사용금액 = 4000 THEN -1 * 1000 * 0.5
                        ELSE 0
                    END) AS 본사_분담액,
                CASE 
                    WHEN YM = '202411' AND brand = "숯불" AND 프로모션_구분 LIKE '%코카콜라%' AND 쿠폰사용금액 = 4000 THEN (-1000) * 0.5
                    ELSE 0
                END AS 분담액_가맹,
                SUM(CASE 
                        WHEN YM = '202411' AND brand = "숯불" AND 프로모션_구분 LIKE '%코카콜라%' AND 쿠폰사용금액 = 4000 THEN -1 * 1000 * 0.5
                        ELSE 0
                    END) AS 합계_가맹,
                '' AS 분담액,
                '' AS 지원금액
            FROM prom_baemin
            WHERE 
                YM = '202411' AND brand = "숯불" AND 프로모션_구분 LIKE '%코카콜라%' AND 쿠폰사용금액 = 4000
            GROUP BY YM, brand, 내용, 금액
            UNION ALL\n
        """
    },
    "shop_detail": {
        "분담금": """
            -- _08_배민_부담금_[코카콜라.숯불]
            WHEN YM IN ('202411') AND brand = '숯불' AND 프로모션_구분 LIKE '%코카콜라%' AND (정산금액 = 4000) THEN ROUND(((정산금액 - 1000) * 0.5), 1)
        """,
        "총합계": """
            -- _08_배민_부담금_[코카콜라.숯불]
            WHEN YM IN ('202411') AND brand = '숯불' AND 프로모션_구분 LIKE '%코카콜라%' AND (정산금액 = 4000) THEN ((정산금액 - 1000) * 0.5) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END)
        """,
        "과금1차": """
            -- _08_배민_부담금_[코카콜라.숯불]
            WHEN YM IN ('202411') AND brand = '숯불' AND 프로모션_구분 LIKE '%코카콜라%' AND (정산금액 = 4000) THEN ((정산금액 - 1000) * 0.5) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END) / 2
        """,
        "과금2차": """
            -- _08_배민_부담금_[코카콜라.숯불]
            WHEN YM IN ('202411') AND brand = '숯불' AND 프로모션_구분 LIKE '%코카콜라%' AND (정산금액 = 4000) THEN ((정산금액 - 1000) * 0.5) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END) / 2
        """
    }
}


_09_배민_부담금_대표메뉴_두찜 = {
    "main_web": {
        "queries1": """
            -- _09_배민_부담금_[대표메뉴.두찜]
            (
                SELECT
                    brand,
                    '배민' AS 업체,
                    프로모션_구분 AS 프로모션,
                    쿠폰사용금액 AS 금액,
                    YM,
                    CONCAT(DATE_FORMAT(MIN(사용일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(사용일자), '%m-%d')) AS 기간,
                    0 AS 쿠폰건수,
                    -1 * (
                        CASE
                            WHEN YM = '202412' AND brand = '두찜' 
                                AND 프로모션_구분 LIKE '%대표메뉴%' 
                                AND 쿠폰사용금액 IN (24800) 
                                THEN 22800 * COUNT(CASE WHEN 정산금액 != 0 THEN 1 END)
                            ELSE 0
                        END
                    ) AS 합계
                FROM
                    prom_baemin
                WHERE
                    YM = '202412' 
                    AND brand = '두찜' 
                    AND 프로모션_구분 LIKE '%대표메뉴%' 
                    AND 쿠폰사용금액 IN (24800)
                GROUP BY
                    brand, 업체, 프로모션, 금액, YM
            )
            UNION ALL\n
        """,
        "queries2": """
            -- _09_배민_부담금_[대표메뉴.두찜]
            WHEN YM IN ('202412') AND brand = '두찜' AND 프로모션_구분 LIKE '%대표메뉴%' AND (쿠폰사용금액 = 24800) THEN ((쿠폰사용금액 - 22800) * 0.5) * (COUNT(CASE WHEN 정산금액 != 0 THEN 1 END))
        """,
        "queries4": """
            -- _09_배민_부담금_[대표메뉴.두찜]
            WHEN YM IN ('202412') AND brand = '두찜' AND 프로모션_구분 LIKE '%대표메뉴%' AND (쿠폰사용금액 = 24800) THEN ((쿠폰사용금액 - 22800) * 0.5) * (COUNT(CASE WHEN 정산금액 != 0 THEN 1 END))
        """
    },
    "report_web": {
        "query1": """
            -- _09_배민_부담금_[대표메뉴.두찜]
            SELECT
                YM,
                brand,
                프로모션_구분,
                CONCAT(DATE_FORMAT(MIN(사용일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(사용일자), '%m-%d')) AS 기간,
                '-' AS 쿠폰건수,
                SUM(CASE 
                        WHEN YM = '202412' AND brand = "두찜" AND 프로모션_구분 LIKE '%대표메뉴%' AND 쿠폰사용금액 IN (24800) THEN -1 * 22800 * 0.5
                        ELSE 0
                    END) AS 본사분담금,
                SUM(CASE 
                        WHEN YM = '202412' AND brand = "두찜" AND 프로모션_구분 LIKE '%대표메뉴%' AND 쿠폰사용금액 IN (24800) THEN -1 * 22800 * 0.5
                        ELSE 0
                    END) AS 가맹점분담금,
                '' AS 광고분담금,
                SUM(CASE 
                        WHEN YM = '202412' AND brand = "두찜" AND 프로모션_구분 LIKE '%대표메뉴%' AND 쿠폰사용금액 IN (24800) THEN -1 * 22800
                        ELSE 0
                    END) AS 합계
            FROM prom_baemin
            WHERE
                YM = '202412' AND brand = "두찜" AND 프로모션_구분 LIKE '%대표메뉴%' AND 쿠폰사용금액 IN (24800)
            GROUP BY YM, brand, 프로모션_구분
            UNION ALL\n    
        """,
        "query2": """
            -- _09_배민_부담금_[대표메뉴.두찜]
            SELECT
                YM,
                brand,
                프로모션_구분 AS 내용,
                CONCAT(DATE_FORMAT(MIN(사용일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(사용일자), '%m-%d')) AS 날짜,
                쿠폰사용금액 AS 금액,
                '-' AS 쿠폰건수_전체,
                SUM(CASE 
                        WHEN YM = '202412' AND brand = "두찜" AND 프로모션_구분 LIKE '%대표메뉴%' AND 쿠폰사용금액 = 24800 THEN -1 * 22800
                        ELSE 0
                    END) AS 납부금액_전체,
                CASE 
                    WHEN YM = '202412' AND brand = "두찜" AND 프로모션_구분 LIKE '%대표메뉴%' AND 쿠폰사용금액 = 24800 THEN (-22800) * 0.5
                    ELSE 0
                END AS 분담액_본사,
                SUM(CASE 
                        WHEN YM = '202412' AND brand = "두찜" AND 프로모션_구분 LIKE '%대표메뉴%' AND 쿠폰사용금액 = 24800 THEN -1 * 22800 * 0.5
                        ELSE 0
                    END) AS 본사_분담액,
                CASE 
                    WHEN YM = '202412' AND brand = "두찜" AND 프로모션_구분 LIKE '%대표메뉴%' AND 쿠폰사용금액 = 24800 THEN (-22800) * 0.5
                    ELSE 0
                END AS 분담액_가맹,
                SUM(CASE 
                        WHEN YM = '202412' AND brand = "두찜" AND 프로모션_구분 LIKE '%대표메뉴%' AND 쿠폰사용금액 = 24800 THEN -1 * 22800 * 0.5
                        ELSE 0
                    END) AS 합계_가맹,
                '' AS 분담액,
                '' AS 지원금액
            FROM prom_baemin
            WHERE 
                YM = '202412' AND brand = "두찜" AND 프로모션_구분 LIKE '%대표메뉴%' AND 쿠폰사용금액 = 24800
            GROUP BY YM, brand, 내용, 금액
            UNION ALL\n
        """
    },
    "shop_detail": {
        "분담금": """
            -- _09_배민_부담금_[대표메뉴.두찜]
            WHEN YM IN ('202412') AND brand = '두찜' AND 프로모션_구분 LIKE '%대표메뉴%' AND (정산금액 = 24800) THEN ROUND(((정산금액 - 22800) * 0.5), 1)
        """,
        "총합계": """
            -- _09_배민_부담금_[대표메뉴.두찜]
            WHEN YM IN ('202412') AND brand = '두찜' AND 프로모션_구분 LIKE '%대표메뉴%' AND (정산금액 = 24800) THEN ((정산금액 - 22800) * 0.5) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END)
        """,
        "과금1차": """
            -- _09_배민_부담금_[대표메뉴.두찜]
            WHEN YM IN ('202412') AND brand = '두찜' AND 프로모션_구분 LIKE '%대표메뉴%' AND (정산금액 = 24800) THEN ((정산금액 - 22800) * 0.5) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END) / 2
        """,
        "과금2차": """
            -- _09_배민_부담금_[대표메뉴.두찜]
            WHEN YM IN ('202412') AND brand = '두찜' AND 프로모션_구분 LIKE '%대표메뉴%' AND (정산금액 = 24800) THEN ((정산금액 - 22800) * 0.5) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END) / 2
        """
    }
}


_10_배민_부담금_고할인딜 = {
    "main_web": {
        "queries1": """
            -- _10_배민_부담금_[고할인딜]
            (
                SELECT
                    brand,
                    '배민' AS 업체,
                    프로모션_구분 AS 프로모션,
                    쿠폰사용금액 AS 금액,
                    YM,
                    CONCAT(DATE_FORMAT(MIN(사용일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(사용일자), '%m-%d')) AS 기간,
                    0 AS 쿠폰건수,
                    -1 * (
                        CASE
                            WHEN 프로모션_구분 LIKE '고할인딜%' AND 쿠폰사용금액 = 8000 
                                THEN (쿠폰사용금액 - 3000) * COUNT(CASE WHEN 정산금액 != 0 THEN 1 END)
                            WHEN 프로모션_구분 LIKE '고할인딜%' AND 쿠폰사용금액 = 7000 
                                THEN (쿠폰사용금액 - 4000) * COUNT(CASE WHEN 정산금액 != 0 THEN 1 END)
                            ELSE 0
                        END
                    ) AS 합계
                FROM
                    prom_baemin
                WHERE
                    YM = '202502' 
                    AND 프로모션_구분 LIKE '고할인딜%'
                GROUP BY
                    brand, 업체, 프로모션, 금액, YM
            )
            UNION ALL\n
        """,
        "queries2": """
            -- _10_배민_부담금_[고할인딜]
            WHEN YM IN ('202502') AND 프로모션_구분 LIKE '고할인딜%' AND (쿠폰사용금액 = 8000) THEN ((3000) * 0.5) * (COUNT(CASE WHEN 정산금액 != 0 THEN 1 END))
            WHEN YM IN ('202502') AND 프로모션_구분 LIKE '고할인딜%' AND (쿠폰사용금액 = 7000) THEN ((4000) * 0.5) * (COUNT(CASE WHEN 정산금액 != 0 THEN 1 END))
        """,
        "queries4": """
            -- _10_배민_부담금_[고할인딜]
            WHEN YM IN ('202502') AND 프로모션_구분 LIKE '고할인딜%' AND (쿠폰사용금액 = 8000) THEN ((3000) * 0.5) * (COUNT(CASE WHEN 정산금액 != 0 THEN 1 END))
            WHEN YM IN ('202502') AND 프로모션_구분 LIKE '고할인딜%' AND (쿠폰사용금액 = 7000) THEN ((4000) * 0.5) * (COUNT(CASE WHEN 정산금액 != 0 THEN 1 END))
        """
    },
    "report_web": {
        "query1": """
            -- _10_배민_부담금_[고할인딜]
            SELECT
                YM,
                brand,
                프로모션_구분,
                CONCAT(DATE_FORMAT(MIN(사용일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(사용일자), '%m-%d')) AS 기간,
                '-' AS 쿠폰건수,
                SUM(CASE 
                        WHEN 프로모션_구분 LIKE '고할인딜%' AND 쿠폰사용금액 = 8000 THEN -1 * (쿠폰사용금액 - 3000) * 0.5
                        WHEN 프로모션_구분 LIKE '고할인딜%' AND 쿠폰사용금액 = 7000 THEN -1 * (쿠폰사용금액 - 4000) * 0.5
                        ELSE 0
                    END) AS 본사분담금,
                SUM(CASE 
                        WHEN 프로모션_구분 LIKE '고할인딜%' AND 쿠폰사용금액 = 8000 THEN -1 * (쿠폰사용금액 - 3000) * 0.5
                        WHEN 프로모션_구분 LIKE '고할인딜%' AND 쿠폰사용금액 = 7000 THEN -1 * (쿠폰사용금액 - 4000) * 0.5
                        ELSE 0
                    END) AS 가맹점분담금,
                '' AS 광고분담금,
                SUM(CASE 
                        WHEN 프로모션_구분 LIKE '고할인딜%' AND 쿠폰사용금액 = 8000 THEN -1 * (쿠폰사용금액 - 3000)
                        WHEN 프로모션_구분 LIKE '고할인딜%' AND 쿠폰사용금액 = 7000 THEN -1 * (쿠폰사용금액 - 4000)
                        ELSE 0
                    END) AS 합계
            FROM prom_baemin
            WHERE 
                (YM >= '202502') AND 프로모션_구분 LIKE '고할인딜%'
            GROUP BY YM, brand, 프로모션_구분
            UNION ALL\n    
        """,
        "query2": """
            -- _10_배민_부담금_[고할인딜]
            SELECT
                YM,
                brand,
                프로모션_구분 AS 내용,
                CONCAT(DATE_FORMAT(MIN(사용일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(사용일자), '%m-%d')) AS 날짜,
                쿠폰사용금액 AS 금액,
                '-' AS 쿠폰건수_전체,
                SUM(CASE 
                        WHEN 프로모션_구분 LIKE '고할인딜%' AND 쿠폰사용금액 = 8000 THEN -1 * (쿠폰사용금액 - 3000)
                        WHEN 프로모션_구분 LIKE '고할인딜%' AND 쿠폰사용금액 = 7000 THEN -1 * (쿠폰사용금액 - 4000)
                        ELSE 0
                    END) AS 납부금액_전체,
                CASE 
                    WHEN 프로모션_구분 LIKE '고할인딜%' AND 쿠폰사용금액 = 8000 THEN -1 * (쿠폰사용금액 - 3000) * 0.5
                    WHEN 프로모션_구분 LIKE '고할인딜%' AND 쿠폰사용금액 = 7000 THEN -1 * (쿠폰사용금액 - 4000) * 0.5
                    ELSE 0
                END AS 분담액_본사,
                SUM(CASE 
                        WHEN 프로모션_구분 LIKE '고할인딜%' AND 쿠폰사용금액 = 8000 THEN -1 * (쿠폰사용금액 - 3000) * 0.5
                        WHEN 프로모션_구분 LIKE '고할인딜%' AND 쿠폰사용금액 = 7000 THEN -1 * (쿠폰사용금액 - 4000) * 0.5
                        ELSE 0
                    END) AS 본사_분담액,
                CASE 
                    WHEN 프로모션_구분 LIKE '고할인딜%' AND 쿠폰사용금액 = 8000 THEN -1 * (쿠폰사용금액 - 3000) * 0.5
                    WHEN 프로모션_구분 LIKE '고할인딜%' AND 쿠폰사용금액 = 7000 THEN -1 * (쿠폰사용금액 - 4000) * 0.5
                    ELSE 0
                END AS 분담액_가맹,
                SUM(CASE 
                        WHEN 프로모션_구분 LIKE '고할인딜%' AND 쿠폰사용금액 = 8000 THEN -1 * (쿠폰사용금액 - 3000) * 0.5
                        WHEN 프로모션_구분 LIKE '고할인딜%' AND 쿠폰사용금액 = 7000 THEN -1 * (쿠폰사용금액 - 4000) * 0.5
                        ELSE 0
                    END) AS 합계_가맹,
                '' AS 분담액,
                '' AS 지원금액
            FROM prom_baemin
            WHERE 
                (YM >= '202502') AND 프로모션_구분 LIKE '고할인딜%'
            GROUP BY YM, brand, 내용, 금액
            UNION ALL\n
        """
    },
    "shop_detail": {
        "분담금": """
            -- _10_배민_부담금_[고할인딜]
            WHEN YM IN ('202502') AND 프로모션_구분 LIKE '고할인딜%' AND (정산금액 = 8000) THEN ROUND(((3000) * 0.5), 1)
            WHEN YM IN ('202502') AND 프로모션_구분 LIKE '고할인딜%' AND (정산금액 = 7000) THEN ROUND(((4000) * 0.5), 1)
        """,
        "총합계": """
            -- _10_배민_부담금_[고할인딜]
            WHEN YM IN ('202502') AND 프로모션_구분 LIKE '고할인딜%' AND (정산금액 = 8000) THEN ((3000) * 0.5) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END)
            WHEN YM IN ('202502') AND 프로모션_구분 LIKE '고할인딜%' AND (정산금액 = 7000) THEN ((4000) * 0.5) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END)
        """,
        "과금1차": """
            -- _10_배민_부담금_[고할인딜]
            WHEN YM IN ('202502') AND 프로모션_구분 LIKE '고할인딜%' AND (정산금액 = 8000) THEN ((3000) * 0.5) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END) / 2
            WHEN YM IN ('202502') AND 프로모션_구분 LIKE '고할인딜%' AND (정산금액 = 7000) THEN ((4000) * 0.5) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END) / 2
        """,
        "과금2차": """
            -- _10_배민_부담금_[고할인딜]
            WHEN YM IN ('202502') AND 프로모션_구분 LIKE '고할인딜%' AND (정산금액 = 8000) THEN ((3000) * 0.5) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END) / 2
            WHEN YM IN ('202502') AND 프로모션_구분 LIKE '고할인딜%' AND (정산금액 = 7000) THEN ((4000) * 0.5) * COUNT(CASE WHEN 쿠폰사용금액 != 0 THEN 1 END) / 2
        """
    }
}


_11_배민_부담금_배민클럽MASS = {
    "main_web": {
        "queries1": """
            -- _11_배민_부담금_[배민클럽MASS]
            (
                SELECT
                    brand,
                    '배민' AS 업체,
                    프로모션_구분 AS 프로모션,
                    쿠폰사용금액 AS 금액,
                    YM,
                    CONCAT(DATE_FORMAT(MIN(사용일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(사용일자), '%m-%d')) AS 기간,
                    0 AS 쿠폰건수,
                    -1 * (
                        CASE
                            WHEN 프로모션_구분 LIKE '%배민클럽 MASS%' AND 쿠폰사용금액 IN (5000) 
                                THEN 2000 * COUNT(CASE WHEN 정산금액 != 0 THEN 1 END)
                            ELSE 0
                        END
                    ) AS 합계
                FROM
                    prom_baemin
                WHERE
                    YM = '202502' 
                    AND 프로모션_구분 LIKE '%배민클럽 MASS%' 
                    AND 쿠폰사용금액 IN (5000)
                GROUP BY
                    brand, 업체, 프로모션, 금액, YM
            )
            UNION ALL\n
        """,
        "queries2": """
            -- _11_배민_부담금_[배민클럽MASS]
            WHEN YM LIKE '%202502%' AND 프로모션_구분 LIKE '%배민클럽 MASS%' AND (쿠폰사용금액 = 5000) THEN ((쿠폰사용금액 - 2000) * 0.5) * (COUNT(CASE WHEN 정산금액 != 0 THEN 1 END))
        """,
        "queries4": """
            -- _11_배민_부담금_[배민클럽MASS]
            WHEN YM LIKE '%202502%' AND 프로모션_구분 LIKE '%배민클럽 MASS%' AND (쿠폰사용금액 = 5000) THEN ((쿠폰사용금액 - 2000) * 0.5) * (COUNT(CASE WHEN 정산금액 != 0 THEN 1 END))
        """
    },
    "report_web": {
        "query1": """
            -- _11_배민_부담금_[배민클럽MASS]
            SELECT
                YM,
                brand,
                프로모션_구분,
                CONCAT(DATE_FORMAT(MIN(사용일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(사용일자), '%m-%d')) AS 기간,
                '-' AS 쿠폰건수,
                SUM(CASE 
                        WHEN 프로모션_구분 LIKE '%배민클럽 MASS%' AND 쿠폰사용금액 IN (5000) THEN -1 * 2000 * 0.5 
                        ELSE 0
                    END) AS 본사분담금,
                SUM(CASE 
                        WHEN 프로모션_구분 LIKE '%배민클럽 MASS%' AND 쿠폰사용금액 IN (5000) THEN -1 * 2000 * 0.5 
                        ELSE 0
                    END) AS 가맹점분담금,
                '' AS 광고분담금,
                SUM(CASE 
                        WHEN 프로모션_구분 LIKE '%배민클럽 MASS%' AND 쿠폰사용금액 IN (5000) THEN -1 * 2000
                        ELSE 0
                    END) AS 합계
            FROM prom_baemin
            WHERE 
                YM = '202502' AND 프로모션_구분 LIKE '%배민클럽 MASS%' AND 쿠폰사용금액 IN (5000)
            GROUP BY YM, brand, 프로모션_구분
            UNION ALL\n 
        """,
        "query2": """
            -- _11_배민_부담금_[배민클럽MASS]
            SELECT
                YM,
                brand,
                프로모션_구분 AS 내용,
                CONCAT(DATE_FORMAT(MIN(사용일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(사용일자), '%m-%d')) AS 날짜,
                쿠폰사용금액 AS 금액,
                '-' AS 쿠폰건수_전체,
                SUM(CASE 
                        WHEN 프로모션_구분 LIKE '%배민클럽 MASS%' AND 쿠폰사용금액 IN (5000) THEN -1 * 2000
                        ELSE 0
                    END) AS 납부금액_전체,
                CASE 
                    WHEN 프로모션_구분 LIKE '%배민클럽 MASS%' AND 쿠폰사용금액 IN (5000) THEN -1 * 2000 * 0.5
                    ELSE 0
                END AS 분담액_본사,
                SUM(CASE 
                        WHEN 프로모션_구분 LIKE '%배민클럽 MASS%' AND 쿠폰사용금액 IN (5000) THEN -1 * 2000 * 0.5
                        ELSE 0
                    END) AS 본사_분담액,
                CASE 
                    WHEN 프로모션_구분 LIKE '%배민클럽 MASS%' AND 쿠폰사용금액 IN (5000) THEN -1 * 2000 * 0.5
                    ELSE 0
                END AS 분담액_가맹,
                SUM(CASE 
                        WHEN 프로모션_구분 LIKE '%배민클럽 MASS%' AND 쿠폰사용금액 IN (5000) THEN -1 * 2000 * 0.5
                        ELSE 0
                    END) AS 합계_가맹,
                '' AS 분담액,
                '' AS 지원금액
            FROM prom_baemin
            WHERE 
                YM = '202502' AND 프로모션_구분 LIKE '%배민클럽 MASS%' AND 쿠폰사용금액 IN (5000) 
            GROUP BY YM, brand, 내용, 금액    
            UNION ALL\n
        """
    },
    "shop_detail": {
        "분담금": """
            -- _11_배민_부담금_[배민클럽MASS]
            WHEN YM = '202502' AND 프로모션_구분 LIKE '%배민클럽 MASS%' AND 정산금액 = 5000 THEN ROUND(((정산금액 - 2000) * 0.5), 1)
        """,
        "총합계": """
            -- _11_배민_부담금_[배민클럽MASS]
            WHEN YM = '202502' AND 프로모션_구분 LIKE '%배민클럽 MASS%' AND 정산금액 = 5000 THEN SUM(쿠폰사용금액 - 2000) * 0.5
        """,
        "과금1차": """
            -- _11_배민_부담금_[배민클럽MASS]
            WHEN YM = '202502' AND 프로모션_구분 LIKE '%배민클럽 MASS%' AND 정산금액 = 5000 THEN (SUM(쿠폰사용금액 - 2000) * 0.5) / 2
        """,
        "과금2차": """
            -- _11_배민_부담금_[배민클럽MASS]
            WHEN YM = '202502' AND 프로모션_구분 LIKE '%배민클럽 MASS%' AND 정산금액 = 5000 THEN (SUM(쿠폰사용금액 - 2000) * 0.5) / 2
        """
    }
}


_12_부담금_test = {
    "main_web": {
        "queries1": """
        """,
        "queries2": """
        """,
        "queries4": """
        """
    },
    "report_web": {
        "query1": """
        """,
        "query2": """
        """
    },
    "shop_detail": {
        "분담금": """
        """,
        "총합계": """
        """,
        "과금1차": """
        """,
        "과금2차": """
        """
    }
}



#선물하기, 쇼핑라이브, 메뉴할인

_배민_선물하기_쇼핑라이브 = {
    "main_web": {
        "queries1": """
            -- 배민 기타(선물하기 쇼핑라이브)
                (
                    SELECT
                        brand,
                        '배민' AS 업체,
                        이벤트구분 AS 프로모션,
                        '-' AS 금액,
                        YM,
                        CONCAT(DATE_FORMAT(MIN(거래일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(거래일자), '%m-%d')) AS 기간,
                        (COUNT(CASE WHEN 구분 = '사용' THEN 1 END) - COUNT(CASE WHEN 구분 = '취소' THEN 1 END)) AS 쿠폰건수,
                        (SUM(브랜드할인부담금) + SUM(상품권이용료) + SUM(부가세)) AS 합계
                    FROM
                        prom_bamin_etc
                    GROUP BY
                        brand, 업체, 프로모션, 금액, YM
                )
                UNION ALL\n
        """,
        "queries2": """
            -- 배민 기타(선물하기 쇼핑라이브)
            (
                SELECT
                    사업자번호,
                    YM,
                    brand,
                    (count(case when 구분 = '사용' then 1 end) - count(case when 구분 = '취소' then 1 end)) as 건수,
                    (
                        SUM(
                            CASE
                                WHEN YM LIKE '%2023%' THEN 브랜드할인부담금 * 0.7
                                WHEN YM >= '202401' AND YM <= '202408' THEN 브랜드할인부담금 * 0.6
                                ELSE 브랜드할인부담금 * 0.5
                            END
                        ) + SUM(상품권이용료) + SUM(부가세)
                    ) as 총합계,
                    '배달의민족' as 업체,
                    이벤트구분 as 프로모션
                    FROM
                    prom_bamin_etc
                GROUP BY
                    사업자번호, YM, brand, 프로모션
            )
            UNION ALL\n
        """,
        "queries4": """
            -- 배민 기타(선물하기 쇼핑라이브) 과세
            (
                SELECT
                    사업자번호,
                    YM,
                    brand,
                    '0' 건수,
                    (
                        SUM(상품권이용료) + SUM(부가세)
                    ) as 총합계,
                    '배달의민족' as 업체,
                    CONCAT(이벤트구분, '(과세)') as 프로모션
                    FROM
                    prom_bamin_etc
                GROUP BY
                    사업자번호, YM, brand, 프로모션
            )
            UNION ALL\n

            -- 배민 기타(선물하기 쇼핑라이브) 면세
            (
                SELECT
                    사업자번호,
                    YM,
                    brand,
                    (count(case when 구분 = '사용' then 1 end) - count(case when 구분 = '취소' then 1 end)) as 건수,
                    (
                        SUM(
                            CASE
                                WHEN YM LIKE '%2023%' THEN 브랜드할인부담금 * 0.7
                                WHEN YM >= '202401' AND YM <= '202408' THEN 브랜드할인부담금 * 0.6
                                ELSE 브랜드할인부담금 * 0.5
                            END
                        )
                    ) as 총합계,
                    '배달의민족' as 업체,
                    CONCAT(이벤트구분, '(면세)') as 프로모션
                    FROM
                    prom_bamin_etc
                GROUP BY
                    사업자번호, YM, brand, 프로모션
            )
            UNION ALL\n
        """
    },
    "report_web": {
        "query1": """
            -- 진행내역 // 배민선물하기(면세), 배민쇼핑라이브(면세)
            SELECT
                YM,
                brand,
                CONCAT(이벤트구분, '(면세)') AS 프로모션_구분,
                CONCAT(DATE_FORMAT(MIN(거래일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(거래일자), '%m-%d')) AS 기간,
                (COUNT(CASE WHEN 구분 = '사용' THEN 1 END) - COUNT(CASE WHEN 구분 = '취소' THEN 1 END)) as 쿠폰건수,
                CASE
                    WHEN YM < '202409' THEN SUM(브랜드할인부담금 * 0.4)
                    WHEN YM >= '202409' THEN SUM(브랜드할인부담금 * 0.5)
                    ELSE 0
                END AS 본사분담금,
                CASE
                    WHEN YM < '202409' THEN SUM(브랜드할인부담금 * 0.6)
                    WHEN YM >= '202409' THEN SUM(브랜드할인부담금 * 0.5)
                    ELSE 0
                END AS 가맹점부담금,
                '' AS 광고분담금,
                (SUM(브랜드할인부담금)) AS 합계
            FROM prom_bamin_etc
            GROUP BY YM, brand, 프로모션_구분
            UNION ALL\n

            -- 진행내역 // 배민선물하기(과세), 배민쇼핑라이브(과세)
            SELECT
                YM,
                brand,
                CONCAT(이벤트구분, '(과세)') AS 프로모션_구분,
                CONCAT(DATE_FORMAT(MIN(거래일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(거래일자), '%m-%d')) AS 기간,
                '0' as 쿠폰건수,
                '0' AS 본사분담금,
                SUM(상품권이용료) + SUM(부가세) AS 가맹점분담금,
                '' AS 광고분담금,
                SUM(상품권이용료) + SUM(부가세) AS 합계
            FROM prom_bamin_etc
            GROUP BY YM, brand, 프로모션_구분
            UNION ALL\n
        """,
        "query2": """
            -- 진행내역 // 배민선물하기(과세), 배민쇼핑라이브(과세) 
            SELECT
                YM,
                brand,
                CONCAT(이벤트구분, '(과세)') AS 내용,
                CONCAT(DATE_FORMAT(MIN(거래일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(거래일자), '%m-%d')) AS 날짜,
                '' AS 금액,
                '' AS 쿠폰건수_전체,
                (SUM(상품권이용료) + SUM(부가세)) AS 납부금액_전체,
                '' AS 분담액_본사,
                '' AS 합계_본사,
                '100%' AS 분담액_가맹,
                (SUM(상품권이용료) + SUM(부가세)) AS 합계_가맹,
                '' AS 분담액,
                '' AS 지원금액
            FROM prom_bamin_etc
            GROUP BY YM, brand, 내용
            UNION ALL\n

            -- 진행내역 // 배민선물하기(면세), 배민쇼핑라이브(면세)
            SELECT
                YM,
                brand,
                CONCAT(이벤트구분, '(면세)') AS 내용,
                CONCAT(DATE_FORMAT(MIN(거래일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(거래일자), '%m-%d')) AS 날짜,
                '' AS 금액,
                (COUNT(CASE WHEN 구분 = '사용' THEN 1 END) - COUNT(CASE WHEN 구분 = '취소' THEN 1 END)) as 쿠폰건수_전체,
                (SUM(브랜드할인부담금)) AS 납부금액_전체,
                CASE
                    WHEN YM < '202409' THEN '40%'
                    ELSE '50%'
                END AS 분담액_본사,
                CASE
                    WHEN YM < '202409' THEN (SUM(브랜드할인부담금)) - FLOOR(SUM(브랜드할인부담금 * 0.6))
                    WHEN YM >= '202409' THEN SUM(브랜드할인부담금 * 0.5)
                    ELSE 0
                END AS 합계_본사,
                CASE
                    WHEN YM < '202409' THEN '60%'
                    ELSE '50%'
                END AS 분담액_가맹,
                CASE
                    WHEN YM < '202409' THEN (SUM(브랜드할인부담금)) - FLOOR(SUM(브랜드할인부담금 * 0.6))
                    WHEN YM >= '202409' THEN SUM(브랜드할인부담금 * 0.5)
                    ELSE 0
                END AS 합계_가맹,
                '' AS 분담액,
                '' AS 지원금액
            FROM prom_bamin_etc
            GROUP BY YM, brand, 내용
            UNION ALL\n
        """
    },
    "shop_detail": {
        "default": """
            -- 배민 기타(선물하기 쇼핑라이브) / 면세
                (SELECT
                    사업자번호,
                    YM,
                    brand,
                    CONCAT(이벤트구분, ' (면세)') as 행사,
                    '-' as 쿠폰,
                    CASE
                        WHEN YM LIKE '%2023%' THEN '70%'
                        WHEN YM >= '202401' AND YM <= '202408' THEN '60%'
                        ELSE '50%'
                    END as 분담금,
                    (COUNT(CASE WHEN 구분 = '사용' THEN 1 END) - COUNT(CASE WHEN 구분 = '취소' THEN 1 END)) as 건수,
                    (
                        SUM(
                            CASE
                                WHEN YM LIKE '%2023%' THEN 브랜드할인부담금 * 0.7
                                WHEN YM >= '202401' AND YM <= '202408' THEN 브랜드할인부담금 * 0.6
                                ELSE 브랜드할인부담금 * 0.5
                            END
                        )
                    ) as 총합계,
                    (
                        SUM(
                            CASE
                                WHEN YM LIKE '%2023%' THEN 브랜드할인부담금 * 0.7
                                WHEN YM >= '202401' AND YM <= '202408' THEN 브랜드할인부담금 * 0.6
                                ELSE 브랜드할인부담금 * 0.5
                            END
                        )
                    ) as 과금1차,
                    0 as 과금2차
                FROM
                    prom_bamin_etc
                WHERE 1=1
                GROUP BY
                    사업자번호, YM, brand, 행사, 쿠폰, 분담금
                )
                UNION ALL\n

                -- 배민 기타(선물하기 쇼핑라이브) / 과세
                (SELECT
                    사업자번호,
                    YM,
                    brand,
                    CONCAT(이벤트구분, ' (과세)') as 행사,
                    '-' as 쿠폰,
                    '-' as 분담금,
                    (COUNT(CASE WHEN 구분 = '사용' THEN 1 END) - COUNT(CASE WHEN 구분 = '취소' THEN 1 END)) as 건수,
                    (
                        SUM(상품권이용료) + SUM(부가세)
                    ) as 총합계,
                    (
                        SUM(상품권이용료) + SUM(부가세)
                    ) as 과금1차,
                    0 as 과금2차
                FROM
                    prom_bamin_etc
                WHERE 1=1
                GROUP BY
                    사업자번호, YM, brand, 행사, 쿠폰, 분담금
                )
                UNION ALL\n
        """
    }
}


_배민_메뉴할인 = {
    "main_web": {
        "queries1": """
            -- 배민 메뉴할인
            (
                SELECT
                    brand,
                    '배민' AS 업체,
                    메뉴할인 AS 프로모션,
                    ABS(메뉴할인금액) AS 금액,
                    YM,
                    CONCAT(DATE_FORMAT(MIN(거래일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(거래일자), '%m-%d')) AS 기간,
                    SUM(할인건수) AS 쿠폰건수,
                    SUM(ABS(할인건수) * 메뉴할인금액) AS '합계'
                FROM
                    prom_baemin_menuhalin
                GROUP BY
                    brand, 업체, 메뉴할인, 금액, YM
            )
            UNION ALL\n
        """,
        "queries2": """
            -- 배민 메뉴할인
            (
                SELECT
                    사업자번호,
                    YM,
                    brand,
                    SUM(할인건수) AS 건수,
                    CASE
                        WHEN YM LIKE '%2023%' AND brand = '떡참' THEN
                            (SUM(ABS(할인건수) * 메뉴할인금액) * 0.5) -- Adjust the ratio for 떡참 in 2023
                        WHEN YM LIKE '%2023%' THEN
                            (SUM(ABS(할인건수) * 메뉴할인금액) * 0.7) -- Adjust the ratio for other brands in 2023
                        WHEN YM >= '202401' AND YM <= '202408' THEN
                            (SUM(ABS(할인건수) * 메뉴할인금액) * 0.6) -- Adjust the ratio for other brands in 202401 - 202408
                        ELSE
                            (SUM(ABS(할인건수) * 메뉴할인금액) * 0.5) -- Adjust the ratio for 202409 and beyond
                    END AS '총합계',
                    '배달의민족' as 업체,
                    메뉴할인 as 프로모션
                FROM
                    prom_baemin_menuhalin
                GROUP BY
                    사업자번호, YM, brand, 프로모션
            )
            UNION ALL\n
        """,
        "queries4": """
            -- 배민 메뉴할인
            (
                SELECT
                    사업자번호,
                    YM,
                    brand,
                    SUM(할인건수) AS 건수,
                    CASE
                        WHEN YM LIKE '%2023%' AND brand = '떡참' THEN
                            (SUM(ABS(할인건수) * 메뉴할인금액) * 0.5) -- Adjust the ratio for 떡참 in 2023
                        WHEN YM LIKE '%2023%' THEN
                            (SUM(ABS(할인건수) * 메뉴할인금액) * 0.7) -- Adjust the ratio for other brands in 2023
                        WHEN YM >= '202401' AND YM <= '202408' THEN
                            (SUM(ABS(할인건수) * 메뉴할인금액) * 0.6) -- Adjust the ratio for other brands in 202401 - 202408
                        ELSE
                            (SUM(ABS(할인건수) * 메뉴할인금액) * 0.5) -- Adjust the ratio for 202409 and beyond
                    END AS '총합계',
                    '배달의민족' as 업체,
                    메뉴할인 as 프로모션
                FROM
                    prom_baemin_menuhalin
                GROUP BY
                    사업자번호, YM, brand, 프로모션
            )
            UNION ALL\n
        """
    },
    "report_web": {
        "query1": """
            -- 진행내역 // 메뉴할인
            SELECT
                YM,
                brand,
                CONCAT(메뉴할인) AS 프로모션_구분,
                CONCAT(DATE_FORMAT(MIN(거래일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(거래일자), '%m-%d')) AS 기간,
                SUM(할인건수) AS 쿠폰건수,
                CASE
                    WHEN ((YM >= '202401' AND YM <= '202408') OR (YM = '202409' AND MONTH(거래일자) = 8)) THEN SUM(ABS(할인건수) * 메뉴할인금액) * 0.4
                    ELSE SUM(ABS(할인건수) * 메뉴할인금액) * 0.5
                END AS 본사분담금,
                CASE
                    WHEN ((YM >= '202401' AND YM <= '202408') OR (YM = '202409' AND MONTH(거래일자) = 8)) THEN SUM(ABS(할인건수) * 메뉴할인금액) * 0.6
                    ELSE SUM(ABS(할인건수) * 메뉴할인금액) * 0.5
                END AS 가맹점분담금,
                '' AS 광고분담금,
                SUM(ABS(할인건수) * 메뉴할인금액) AS 합계
                FROM prom_baemin_menuhalin
                GROUP BY YM, brand, 메뉴할인, 거래일자
        """,
        "query2": """
            -- 진행내역 // 메뉴할인
            SELECT
                YM,
                brand,
                메뉴할인 AS 내용,
                CONCAT(DATE_FORMAT(MIN(거래일자), '%m-%d'), ' ~ ', DATE_FORMAT(MAX(거래일자), '%m-%d')) AS 날짜,
                ABS(메뉴할인금액) AS 금액,
                SUM(할인건수) AS 쿠폰건수_전체,
                SUM(ABS(할인건수) * 메뉴할인금액) AS 납부금액_전체,
                CASE
                    WHEN (YM >= '202401' AND YM <= '202408') THEN SUM(ABS(할인건수) * 메뉴할인금액) * 0.4
                    ELSE SUM(ABS(할인건수) * 메뉴할인금액) * 0.5
                END AS 분담액_본사,
                CASE
                    WHEN (YM >= '202401' AND YM <= '202408') THEN SUM(ABS(할인건수) * 메뉴할인금액) * 0.4
                    ELSE SUM(ABS(할인건수) * 메뉴할인금액) * 0.5
                END AS 합계_본사,
                CASE
                    WHEN (YM >= '202401' AND YM <= '202408') THEN SUM(ABS(할인건수) * 메뉴할인금액) * 0.6
                    ELSE SUM(ABS(할인건수) * 메뉴할인금액) * 0.5
                END AS 분담액_가맹,
                CASE
                    WHEN (YM >= '202401' AND YM <= '202408') THEN SUM(ABS(할인건수) * 메뉴할인금액) * 0.6
                    ELSE SUM(ABS(할인건수) * 메뉴할인금액) * 0.5
                END AS 합계_가맹,
                '' AS 분담액,
                '' AS 지원금액
            FROM prom_baemin_menuhalin
            GROUP BY YM, brand, 내용, 금액
        """
    },
    "shop_detail": {
        "default": """
            -- 배민 메뉴할인
            (SELECT
                사업자번호,
                YM,
                brand,
                메뉴할인 AS 행사,
                ABS(메뉴할인금액) AS 쿠폰,
                CASE
                    WHEN YM LIKE '%2023%' AND brand = '떡참' THEN
                        ROUND((ABS(메뉴할인금액) * 0.5), 1) -- Adjust the ratio for 떡참 in 2023
                    WHEN YM LIKE '%2023%' THEN
                        ROUND((ABS(메뉴할인금액) * 0.7), 1) -- Adjust the ratio for other brands in 2023
                    WHEN YM >= '202401' AND YM <= '202408' THEN
                        ROUND((ABS(메뉴할인금액) * 0.6), 1) -- Adjust the ratio for other brands in 202401 - 202408
                    ELSE
                        ROUND((ABS(메뉴할인금액) * 0.5), 1) -- Adjust the ratio for 202409 and beyond
                END AS 분담금,
                SUM(할인건수) AS 건수,
                CASE
                    WHEN YM LIKE '%2023%' AND brand = '떡참' THEN
                        (SUM(ABS(할인건수) * 메뉴할인금액) * 0.5) -- Adjust the ratio for 떡참 in 2023
                    WHEN YM LIKE '%2023%' THEN
                        (SUM(ABS(할인건수) * 메뉴할인금액) * 0.7) -- Adjust the ratio for other brands in 2023
                    WHEN YM >= '202401' AND YM <= '202408' THEN
                        (SUM(ABS(할인건수) * 메뉴할인금액) * 0.6) -- Adjust the ratio for other brands in 202401 - 202408
                    ELSE
                        (SUM(ABS(할인건수) * 메뉴할인금액) * 0.5) -- Adjust the ratio for 202409 and beyond
                END AS '총합계',
                CASE
                    WHEN YM LIKE '%2023%' AND brand = '떡참' THEN
                        (SUM(ABS(할인건수) * 메뉴할인금액) * 0.5) / 2 -- Adjust the ratio for 떡참 in 2023
                    WHEN YM LIKE '%2023%' THEN
                        (SUM(ABS(할인건수) * 메뉴할인금액) * 0.7) / 2 -- Adjust the ratio for other brands in 2023
                    WHEN YM >= '202401' AND YM <= '202408' THEN
                        (SUM(ABS(할인건수) * 메뉴할인금액) * 0.6) / 2 -- Adjust the ratio for other brands in 202401 - 202408
                    ELSE
                        (SUM(ABS(할인건수) * 메뉴할인금액) * 0.5) / 2 -- Adjust the ratio for 202409 and beyond
                END AS '과금1차',
                CASE
                    WHEN YM LIKE '%2023%' AND brand = '떡참' THEN
                        (SUM(ABS(할인건수) * 메뉴할인금액) * 0.5) / 2 -- Adjust the ratio for 떡참 in 2023
                    WHEN YM LIKE '%2023%' THEN
                        (SUM(ABS(할인건수) * 메뉴할인금액) * 0.7) / 2 -- Adjust the ratio for other brands in 2023
                    WHEN YM >= '202401' AND YM <= '202408' THEN
                        (SUM(ABS(할인건수) * 메뉴할인금액) * 0.6) / 2 -- Adjust the ratio for other brands in 202401 - 202408
                    ELSE
                        (SUM(ABS(할인건수) * 메뉴할인금액) * 0.5) / 2 -- Adjust the ratio for 202409 and beyond
                END AS '과금2차'
            FROM
                prom_baemin_menuhalin
            WHERE 1=1
            GROUP BY
                사업자번호, YM, brand, 행사, 쿠폰, 분담금
            )
            UNION ALL\n
        """
    }
}




def queryPatten(main_web, queries1, option="partial"):
    # 패턴에 맞는 변수 찾기
    if option == "partial":
        pattern = re.compile(r"^_\d{2}_")
    elif option == "all":
        pattern = re.compile(r"")
    result = ""

    # 먼저 globals()의 복사본을 리스트로 저장
    global_vars = list(globals().items())

    for var_name, var_value in global_vars:
        if pattern.match(var_name) and isinstance(var_value, dict):
            if main_web in var_value and queries1 in var_value[main_web]:
                result += str(var_value[main_web][queries1]) + "\n"

    # # 문자열을 파일로 저장
    # with open("output.txt", "w", encoding="utf-8") as f:
    #     f.write(result.strip())  # 마지막 개행 문자 제거

    return result


if __name__ == "__main__":
    # 예제 실행
    # print(queryPatten("main_web", "queries1", "partial"))
    print(queryPatten("report_web", "query1", "all"))
