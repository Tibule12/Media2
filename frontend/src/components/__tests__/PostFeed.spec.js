import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import PostFeed from '../PostFeed.vue';

describe('PostFeed.vue', () => {
  it('renders post feed container', () => {
    const wrapper = mount(PostFeed);
    expect(wrapper.find('.post-feed').exists()).toBe(true);
  });
});
