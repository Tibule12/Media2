import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, Image, StyleSheet, TouchableOpacity } from 'react-native';
import axios from 'axios';

export default function PostFeedScreen() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/posts/?sort=newest');
      setPosts(response.data);
    } catch (error) {
      console.error('Failed to load posts', error);
    }
  };

  const renderItem = ({ item }) => (
    <View style={styles.post}>
      <Text style={styles.author}>{item.author.username}</Text>
      <Text style={styles.content}>{item.content}</Text>
      <View style={styles.mediaContainer}>
        {item.media.map(media => (
          media.media_type === 'image' ? (
            <Image key={media.id} source={{ uri: `http://localhost:8000/media/${media.file}` }} style={styles.image} />
          ) : media.media_type === 'video' ? (
            <Text key={media.id} style={styles.videoPlaceholder}>[Video content]</Text>
          ) : null
        ))}
      </View>
      <Text>Likes: {item.likes ? item.likes.length : 0}</Text>
    </View>
  );

  return (
    <View style={styles.container}>
      <FlatList
        data={posts}
        keyExtractor={item => item.id.toString()}
        renderItem={renderItem}
        ListEmptyComponent={<Text>No posts yet.</Text>}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 10,
  },
  post: {
    borderWidth: 1,
    borderColor: '#ccc',
    padding: 10,
    marginBottom: 10,
  },
  author: {
    fontWeight: 'bold',
    marginBottom: 5,
  },
  content: {
    marginBottom: 5,
  },
  mediaContainer: {
    marginBottom: 5,
  },
  image: {
    width: '100%',
    height: 200,
    resizeMode: 'cover',
  },
  videoPlaceholder: {
    fontStyle: 'italic',
    color: '#888',
  },
});
