import xml.etree.ElementTree as ET


class YouTubeParser:
    NS = {
        "atom": "http://www.w3.org/2005/Atom",
        "yt": "http://www.youtube.com/xml/schemas/2015",
    }

    @classmethod
    def parse_websub_xml(cls, xml_body: str):
        root = ET.fromstring(xml_body)

        entry = root.find("atom:entry", cls.NS)
        if entry is None:
            return None

        video_id = entry.findtext("yt:videoId", default="", namespaces=cls.NS)
        channel_id = entry.findtext("yt:channelId", default="", namespaces=cls.NS)
        title = entry.findtext("atom:title", default="", namespaces=cls.NS)
        published = entry.findtext("atom:published", default="", namespaces=cls.NS)
        updated = entry.findtext("atom:updated", default="", namespaces=cls.NS)

        if not video_id or not channel_id:
            return None

        return {
            "video_id": video_id,
            "channel_id": channel_id,
            "title": title,
            "published": published,
            "updated": updated,
            "url": f"https://youtu.be/{video_id}",
        }